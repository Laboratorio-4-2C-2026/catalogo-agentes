from dataclasses import dataclass
from datetime import date
from enum import Enum

from .tablero import DOMAIN_AREAS, GENERAL_AREA, Incident, KeyActivity, Tablero, WeekColumn
from .workbook import column_letter, comparable_text

GREEN = "verde"
YELLOW = "amarillo"
RED = "rojo"
FINISHED = "finaliz."
IN_PROGRESS = "en curso"
OPEN = "abierto"
CLOSED = "cerrado"
HIGH_CRITICALITY = "alta"
# From the 27-08 class: "si ven que está todo en verde 3 semanas seguidas sospechan".
SUSPICIOUS_GREEN_WEEKS = 3
YELLOWS_THAT_MAKE_GENERAL_RED = 3


class FindingKind(Enum):
    MISSING = "missing"
    INCONSISTENT = "inconsistent"
    OVERDUE = "overdue"
    ATTENTION = "attention"


@dataclass(frozen=True)
class Finding:
    kind: FindingKind
    location: str
    message: str


def current_week(tablero: Tablero, as_of: date) -> WeekColumn:
    started_weeks = [week for week in tablero.weeks if week.monday <= as_of]
    return max(started_weeks, key=lambda week: week.number)


def last_loaded_week(tablero: Tablero) -> int | None:
    loaded = [number for area in tablero.areas.values() for number in area.statuses]
    return max(loaded, default=None)


def expected_general(domain_statuses: list[str]) -> str:
    """The rule printed on the RESUMEN tab of the Tablero."""
    statuses = [comparable_text(status) for status in domain_statuses]
    if RED in statuses or statuses.count(YELLOW) >= YELLOWS_THAT_MAKE_GENERAL_RED:
        return "Rojo"
    if YELLOW in statuses:
        return "Amarillo"
    return "Verde"


def find_gaps(tablero: Tablero, as_of: date) -> list[Finding]:
    week = current_week(tablero, as_of)
    return [
        *_missing_statuses(tablero, up_to=week),
        *_general_mismatches(tablero),
        *_unexplained_warnings(tablero),
        *_suspicious_green(tablero),
        *_missing_summary(tablero),
        *(finding for activity in tablero.activities for finding in _activity_findings(activity, as_of)),
        *(finding for incident in tablero.incidents for finding in _incident_findings(incident, as_of)),
        *_invalid_values(tablero),
        *_missing_product_url(tablero),
    ]


def _missing_statuses(tablero: Tablero, *, up_to: WeekColumn) -> list[Finding]:
    findings = []
    for week in tablero.weeks:
        if week.number > up_to.number:
            break
        missing = [area for area in (GENERAL_AREA, *DOMAIN_AREAS) if not _status(tablero, area, week.number)]
        if missing:
            findings.append(Finding(
                FindingKind.MISSING,
                f"column {week.letter} (Sem-{week.number:02d}, {week.monday:%d/%m})",
                f"no status for {', '.join(missing)}",
            ))
    return findings


def _general_mismatches(tablero: Tablero) -> list[Finding]:
    findings = []
    for week in tablero.weeks:
        domain_statuses = [_status(tablero, area, week.number) for area in DOMAIN_AREAS]
        general = _status(tablero, GENERAL_AREA, week.number)
        if not all(domain_statuses) or not general:
            continue
        expected = expected_general(domain_statuses)
        if comparable_text(general) != comparable_text(expected):
            findings.append(Finding(
                FindingKind.INCONSISTENT,
                f"{week.letter}{tablero.areas[GENERAL_AREA].row} (Sem-{week.number:02d})",
                f"General is {general} but the RESUMEN rule gives {expected} for {', '.join(domain_statuses)}",
            ))
    return findings


def _unexplained_warnings(tablero: Tablero) -> list[Finding]:
    latest = last_loaded_week(tablero)
    if latest is None:
        return []
    findings = []
    for area in tablero.areas.values():
        status = area.status_in(latest)
        if comparable_text(status) in (YELLOW, RED) and not (area.reason and area.action):
            cells = f"{column_letter(tablero.reason_column)}{area.row}/{column_letter(tablero.action_column)}{area.row}"
            findings.append(Finding(
                FindingKind.MISSING,
                cells,
                f"{area.area} is {status} in Sem-{latest:02d} but Motivo or Acción tomada is empty",
            ))
    return findings


def _suspicious_green(tablero: Tablero) -> list[Finding]:
    findings = []
    general = tablero.areas.get(GENERAL_AREA)
    if general and _trailing_green_weeks(general.statuses) >= SUSPICIOUS_GREEN_WEEKS:
        findings.append(Finding(
            FindingKind.ATTENTION,
            f"row {general.row} (General)",
            f"General has been Verde for {_trailing_green_weeks(general.statuses)} weeks in a row; "
            "the professors said three straight green weeks makes them suspect a hidden problem",
        ))
    for area in (tablero.areas[name] for name in DOMAIN_AREAS if name in tablero.areas):
        if len(area.statuses) > SUSPICIOUS_GREEN_WEEKS and _trailing_green_weeks(area.statuses) == len(area.statuses):
            findings.append(Finding(
                FindingKind.ATTENTION,
                f"row {area.row} ({area.area})",
                f"{area.area} has never left Verde in {len(area.statuses)} loaded weeks; check it against what happened",
            ))
    return findings


def _trailing_green_weeks(statuses: dict[int, str]) -> int:
    streak = 0
    for week_number in sorted(statuses, reverse=True):
        if comparable_text(statuses[week_number]) != GREEN:
            break
        streak += 1
    return streak


def _missing_summary(tablero: Tablero) -> list[Finding]:
    findings = []
    if tablero.overall_progress in (None, ""):
        findings.append(Finding(FindingKind.MISSING, "Avance Global [%]", "never filled"))
    if tablero.expected_end in (None, ""):
        findings.append(Finding(FindingKind.MISSING, "Fecha de Fin Prevista", "never filled"))
    return findings


def _activity_findings(activity: KeyActivity, as_of: date) -> list[Finding]:
    location = f"row {activity.row} ({activity.name})"
    return [
        Finding(kind, location, message)
        for kind, message in (
            *_activity_state_problems(activity),
            *_activity_date_problems(activity, as_of),
            *_activity_deviation_problems(activity),
        )
    ]


def _activity_state_problems(activity: KeyActivity) -> list[tuple[FindingKind, str]]:
    state = comparable_text(activity.state)
    if not state:
        return [(FindingKind.MISSING, "no Estado Tarea")]
    if state == FINISHED and activity.progress != 1:
        return [(FindingKind.INCONSISTENT, f"Finaliz. with Avance {_percent(activity.progress)}")]
    if state == IN_PROGRESS and not activity.progress:
        return [(FindingKind.ATTENTION, "En curso at 0%: either it has not started or the percentage is stale")]
    return []


def _activity_date_problems(activity: KeyActivity, as_of: date) -> list[tuple[FindingKind, str]]:
    finished = comparable_text(activity.state) == FINISHED
    if activity.baseline_end is None:
        return [(FindingKind.MISSING, "no F. Fin L. Base")]
    if finished and activity.actual_end is None:
        return [(FindingKind.MISSING, "Finaliz. without F. Fin Real")]
    if not finished and activity.actual_end is not None:
        return [(FindingKind.INCONSISTENT, f"has F. Fin Real {activity.actual_end:%d/%m} but is not Finaliz.")]
    expected_end = activity.estimated_end or activity.baseline_end
    if not finished and expected_end < as_of:
        return [(FindingKind.OVERDUE, f"F. Fin Estimado {expected_end:%d/%m} has passed and it is not finished")]
    return []


def _activity_deviation_problems(activity: KeyActivity) -> list[tuple[FindingKind, str]]:
    if activity.baseline_end is None or activity.actual_end is None:
        return []
    expected_days = _days_ahead_of_baseline(activity)
    if activity.deviation_days is None:
        return [] if expected_days == 0 else [(FindingKind.MISSING, f"Desvío empty, base minus real gives {expected_days:+d} days")]
    if activity.deviation_days != expected_days:
        return [(FindingKind.INCONSISTENT, f"Desvío {activity.deviation_days:+.0f} but base minus real gives {expected_days:+d}")]
    return []


def _days_ahead_of_baseline(activity: KeyActivity) -> int:
    """The cátedra's template computes Desvío as F. Fin L. Base minus F. Fin Real, and only once there is a real end,
    so a positive value means finished early and an open activity has none."""
    return (activity.baseline_end - activity.actual_end).days


def _incident_findings(incident: Incident, as_of: date) -> list[Finding]:
    location = f"row {incident.row} ({incident.description[:50]})"
    state = comparable_text(incident.state)
    problems = []
    if not incident.criticality:
        problems.append((FindingKind.MISSING, "no Criticidad"))
    if incident.opened is None:
        problems.append((FindingKind.MISSING, "no F. Alta"))
    if state == CLOSED and incident.closed is None:
        problems.append((FindingKind.MISSING, "Cerrado without F. Cierre"))
    if state == OPEN:
        problems.extend(_open_incident_problems(incident, as_of))
    return [Finding(kind, location, message) for kind, message in problems]


def _open_incident_problems(incident: Incident, as_of: date) -> list[tuple[FindingKind, str]]:
    problems = []
    if incident.due is None:
        problems.append((FindingKind.MISSING, "open without F. Límite"))
    elif incident.due < as_of:
        problems.append((FindingKind.OVERDUE, f"open past its F. Límite {incident.due:%d/%m}"))
    if comparable_text(incident.criticality) == HIGH_CRITICALITY:
        problems.append((FindingKind.ATTENTION, "Criticidad Alta means escalating it to the professors"))
    return problems


def _invalid_values(tablero: Tablero) -> list[Finding]:
    checks = [
        ("semaforo", "status", [(f"row {area.row}", status) for area in tablero.areas.values() for status in area.statuses.values()]),
        ("estado tarea", "Estado Tarea", [(f"row {activity.row}", activity.state) for activity in tablero.activities]),
        ("estado", "incident Estado", [(f"row {incident.row}", incident.state) for incident in tablero.incidents]),
        ("criticidad", "Criticidad", [(f"row {incident.row}", incident.criticality) for incident in tablero.incidents]),
    ]
    findings = []
    for list_name, field_name, located_values in checks:
        allowed = {comparable_text(value) for value in tablero.allowed_values.get(list_name, ())}
        for location, value in located_values:
            if allowed and value and comparable_text(value) not in allowed:
                findings.append(Finding(FindingKind.INCONSISTENT, location, f"{field_name} {value!r} is not in the listas tab"))
    return findings


def _missing_product_url(tablero: Tablero) -> list[Finding]:
    return [] if tablero.product_url else [Finding(FindingKind.MISSING, "PRODUCTO > URL", "empty")]


def _status(tablero: Tablero, area: str, week_number: int) -> str:
    row = tablero.areas.get(area)
    return row.status_in(week_number) if row else ""


def _percent(progress: float | None) -> str:
    return "empty" if progress is None else f"{progress:.0%}"
