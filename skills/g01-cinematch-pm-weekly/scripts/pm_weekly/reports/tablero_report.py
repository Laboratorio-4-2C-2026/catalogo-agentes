from ..spreadsheets.tablero import DOMAIN_AREAS, GENERAL_AREA, Tablero, WeekColumn
from ..spreadsheets.tablero_checks import Finding, FindingKind

WEEKS_OF_HISTORY = 4


def print_tablero(tablero: Tablero, current: WeekColumn, findings: list[Finding]) -> None:
    print(f"Tablero tab {tablero.tab!r} · PM: {tablero.project_manager or '(empty)'}")
    print(f"This week's column: {current.letter} (Sem-{current.number:02d}, report date {current.monday:%d/%m})")
    print()
    _print_status_history(tablero, current)
    print()
    _print_summary_fields(tablero)
    print()
    _print_activities(tablero)
    print()
    _print_incidents(tablero)
    print()
    _print_findings(findings)


def _print_status_history(tablero: Tablero, current: WeekColumn) -> None:
    weeks = [week for week in tablero.weeks if current.number - WEEKS_OF_HISTORY < week.number <= current.number]
    print("Area".ljust(12) + "".join(f"Sem-{week.number:02d}".ljust(11) for week in weeks) + "Motivo / Acción")
    for area_name in (GENERAL_AREA, *DOMAIN_AREAS):
        area = tablero.areas.get(area_name)
        if area is None:
            print(f"{area_name.ljust(12)}(row not found)")
            continue
        statuses = "".join((area.status_in(week.number) or "-").ljust(11) for week in weeks)
        explanation = " / ".join(text for text in (area.reason, area.action) if text) or "-"
        print(f"{area_name.ljust(12)}{statuses}{explanation}")


def _print_summary_fields(tablero: Tablero) -> None:
    print(f"Avance Global [%]: {_shown(tablero.overall_progress)}")
    print(f"Fecha de Fin Prevista: {_shown(tablero.expected_end)}")
    print(f"Producto URL: {tablero.product_url or '(empty)'}")


def _print_activities(tablero: Tablero) -> None:
    print("Actividades clave (row · estado · avance · base / estimado / real · desvío)")
    for activity in tablero.activities:
        progress = "-" if activity.progress is None else f"{activity.progress:.0%}"
        dates = " / ".join(_day(day) for day in (activity.baseline_end, activity.estimated_end, activity.actual_end))
        deviation = "-" if activity.deviation_days is None else f"{activity.deviation_days:+.0f}"
        print(f"  {activity.row:>3} {activity.name[:42].ljust(42)} {activity.state or '-':9} {progress:>5}  {dates}  {deviation}")


def _print_incidents(tablero: Tablero) -> None:
    print("Incidentes (row · estado · criticidad · alta / límite / cierre)")
    for incident in tablero.incidents:
        dates = " / ".join(_day(day) for day in (incident.opened, incident.due, incident.closed))
        print(f"  {incident.row:>3} {incident.description[:55].ljust(55)} {incident.state or '-':8} {incident.criticality or '-':6} {dates}")


def _print_findings(findings: list[Finding]) -> None:
    if not findings:
        print("No gaps found.")
        return
    for kind in FindingKind:
        of_kind = [finding for finding in findings if finding.kind == kind]
        if of_kind:
            print(f"{kind.value.upper()} ({len(of_kind)})")
            for finding in of_kind:
                print(f"  - {finding.location}: {finding.message}")


def _shown(value) -> str:
    return "(empty)" if value in (None, "") else str(value)


def _day(day) -> str:
    return day.strftime("%d/%m") if day else "-"
