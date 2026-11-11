import re
from dataclasses import dataclass
from datetime import date

from .workbook import (
    CellPosition,
    SheetGrid,
    as_date,
    as_number,
    column_letter,
    column_starting_with,
    comparable_text,
    require_sheet,
    visible_text,
)

GENERAL_AREA = "General"
DOMAIN_AREAS = ("Alcance", "Cronograma", "Incidentes", "Calidad", "Riesgos")
ALLOWED_VALUES_TAB = "listas"

WEEK_HEADER = re.compile(
    r"""
    (?P<day>\d{1,2}) / (?P<month>\d{1,2})   # the week's report Monday, dd/mm
    \s* sem- (?P<number>\d+)                 # the week number, Sem-01 to Sem-20
    """,
    re.VERBOSE | re.IGNORECASE,
)


@dataclass(frozen=True)
class WeekColumn:
    number: int
    monday: date
    column: int

    @property
    def letter(self) -> str:
        return column_letter(self.column)


@dataclass(frozen=True)
class AreaRow:
    area: str
    row: int
    statuses: dict[int, str]
    reason: str
    action: str

    def status_in(self, week_number: int) -> str:
        return self.statuses.get(week_number, "")


@dataclass(frozen=True)
class KeyActivity:
    row: int
    name: str
    state: str
    progress: float | None
    baseline_end: date | None
    estimated_end: date | None
    actual_end: date | None
    deviation_days: float | None
    comment: str


@dataclass(frozen=True)
class Incident:
    row: int
    description: str
    state: str
    criticality: str
    opened: date | None
    due: date | None
    closed: date | None
    resolution: str


@dataclass(frozen=True)
class Tablero:
    tab: str
    project_manager: str
    weeks: tuple[WeekColumn, ...]
    areas: dict[str, AreaRow]
    reason_column: int
    action_column: int
    overall_progress: object
    expected_end: object
    activities: tuple[KeyActivity, ...]
    activity_rows: range
    incidents: tuple[Incident, ...]
    incident_rows: range
    product_url: str
    allowed_values: dict[str, frozenset[str]]

    def week(self, number: int) -> WeekColumn | None:
        return next((week for week in self.weeks if week.number == number), None)


def read_tablero(book, tab: str, *, year: int) -> Tablero:
    grid = SheetGrid(require_sheet(book, tab))
    status_header = grid.require("ÁREA")
    weeks = _week_columns(grid, status_header.row, year)
    status_columns = _ColumnFinder(grid, status_header.row)
    reason_column = status_columns.find("Motivo")
    action_column = status_columns.find("Acción")
    activity_header, activity_rows = _activity_block(grid)
    incident_header, incident_rows = _incident_block(grid)
    return Tablero(
        tab=tab,
        project_manager=visible_text(grid.value_right_of(grid.require("PM:"))),
        weeks=weeks,
        areas=_area_rows(grid, status_header, weeks, reason_column=reason_column, action_column=action_column),
        reason_column=reason_column,
        action_column=action_column,
        overall_progress=grid.value_right_of(grid.require("Avance Global [%]"), stop_at_labels=("Fecha de Fin Prevista",)),
        expected_end=grid.value_right_of(grid.require("Fecha de Fin Prevista")),
        activities=_key_activities(grid, activity_header, activity_rows),
        activity_rows=activity_rows,
        incidents=_incidents(grid, incident_header, incident_rows),
        incident_rows=incident_rows,
        product_url=visible_text(grid.value_right_of(grid.require("URL:"))),
        allowed_values=_allowed_values(book),
    )


def _week_columns(grid: SheetGrid, header_row: int, year: int) -> tuple[WeekColumn, ...]:
    weeks = []
    for column in range(1, grid.last_column + 1):
        match = WEEK_HEADER.search(grid.text(header_row, column))
        if match:
            monday = date(year, int(match["month"]), int(match["day"]))
            weeks.append(WeekColumn(int(match["number"]), monday, column))
    return tuple(weeks)


def _area_rows(
    grid: SheetGrid,
    status_header: CellPosition,
    weeks: tuple[WeekColumn, ...],
    *,
    reason_column: int,
    action_column: int,
) -> dict[str, AreaRow]:
    wanted_areas = {comparable_text(area): area for area in (GENERAL_AREA, *DOMAIN_AREAS)}
    areas = {}
    for row in range(status_header.row + 1, status_header.row + 1 + 2 * len(wanted_areas)):
        area = wanted_areas.get(comparable_text(grid.value(row, status_header.column)))
        if area:
            areas[area] = AreaRow(
                area=area,
                row=row,
                statuses={week.number: grid.text(row, week.column) for week in weeks if grid.text(row, week.column)},
                reason=grid.text(row, reason_column),
                action=grid.text(row, action_column),
            )
    return areas


def _activity_block(grid: SheetGrid) -> tuple[CellPosition, range]:
    header = grid.require("Actividades Clave")
    section_end = grid.require("INCIDENTES", after_row=header.row).row
    return header, range(header.row + 1, section_end)


def _incident_block(grid: SheetGrid) -> tuple[CellPosition, range]:
    section = grid.require("INCIDENTES", after_row=grid.require("Actividades Clave").row)
    header = grid.require("Descripción", after_row=section.row)
    section_end = grid.require("PRODUCTO", after_row=header.row).row
    return header, range(header.row + 1, section_end)


def _key_activities(grid: SheetGrid, header: CellPosition, rows: range) -> tuple[KeyActivity, ...]:
    columns = _ColumnFinder(grid, header.row)
    return tuple(
        KeyActivity(
            row=row,
            name=grid.text(row, header.column),
            state=grid.text(row, columns.find("Estado")),
            progress=as_number(grid.value(row, columns.find("Avance"))),
            baseline_end=as_date(grid.value(row, columns.find("F. Fin L. Base"))),
            estimated_end=as_date(grid.value(row, columns.find("F. Fin Estimado"))),
            actual_end=as_date(grid.value(row, columns.find("F. Fin Real"))),
            deviation_days=as_number(grid.value(row, columns.find("Desvío"))),
            comment=grid.text(row, columns.find("Comentarios")),
        )
        for row in rows
        if grid.text(row, header.column)
    )


def _incidents(grid: SheetGrid, header: CellPosition, rows: range) -> tuple[Incident, ...]:
    columns = _ColumnFinder(grid, header.row)
    return tuple(
        Incident(
            row=row,
            description=grid.text(row, header.column),
            state=grid.text(row, columns.find("Estado")),
            criticality=grid.text(row, columns.find("Criticidad")),
            opened=as_date(grid.value(row, columns.find("F. Alta"))),
            due=as_date(grid.value(row, columns.find("F. Límite"))),
            closed=as_date(grid.value(row, columns.find("F. Cierre"))),
            resolution=grid.text(row, columns.find("Resolución")),
        )
        for row in rows
        if grid.text(row, header.column)
    )


def _allowed_values(book) -> dict[str, frozenset[str]]:
    if ALLOWED_VALUES_TAB not in book.sheetnames:
        return {}
    grid = SheetGrid(book[ALLOWED_VALUES_TAB])
    return {
        comparable_text(grid.value(1, column)): frozenset(
            grid.text(row, column) for row in range(2, grid.last_row + 1) if grid.text(row, column)
        )
        for column in range(1, grid.last_column + 1)
        if grid.text(1, column)
    }


class _ColumnFinder:
    def __init__(self, grid: SheetGrid, header_row: int):
        self._headers = grid.headers(header_row)
        self._sheet_title = grid.sheet.title

    def find(self, prefix: str) -> int:
        return column_starting_with(self._headers, prefix, sheet_title=self._sheet_title)
