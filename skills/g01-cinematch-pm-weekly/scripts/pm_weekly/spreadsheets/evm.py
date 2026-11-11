import re
from dataclasses import dataclass

from .workbook import LayoutChanged, SheetGrid, as_number, cell_reference, column_letter, comparable_text, require_sheet

PERIOD_HEADER = re.compile(
    r"""
    ^(?:p|periodo\s*)   # "P9" in the team's workbook, "Periodo 9" in the cátedra's
    (?P<number>\d+)$
    """,
    re.VERBOSE,
)
MINIMUM_PERIOD_COLUMNS = 3
PLANNED_LABEL = "valor planeado"
EARNED_LABEL = "valor ganado"
ACTUAL_LABEL = "costo real"
PREFERRED_UNIT = "hh"
ORIGINAL_PLAN_LABEL = "PV acum. linea base ORIGINAL"


@dataclass(frozen=True)
class EvmSeries:
    label: str
    row: int
    unit: str
    values: dict[int, float]

    def last_period(self) -> int | None:
        return max(self.values, default=None)

    def cumulative_until(self, period: int) -> float:
        return sum(value for number, value in self.values.items() if number <= period)


@dataclass(frozen=True)
class EvmSheet:
    title: str
    periods: tuple[int, ...]
    period_columns: dict[int, int]
    planned: EvmSeries
    earned: EvmSeries | None
    actual: EvmSeries | None

    @property
    def budget_at_completion(self) -> float:
        return sum(self.planned.values.values())

    @property
    def last_loaded_period(self) -> int | None:
        """The last period with both EV and AC, which is where the workbook's cut has to point."""
        if self.earned is None or self.actual is None:
            return None
        loaded = set(self.earned.values) & set(self.actual.values)
        return max(loaded, default=None)

    def input_cell(self, series: EvmSeries, period: int) -> str:
        return cell_reference(self.title, f"{column_letter(self.period_columns[period])}{series.row}")

    def periods_missing_until(self, period: int) -> list[int]:
        return [
            number
            for number in self.periods
            if number <= period and any(series is None or number not in series.values for series in (self.earned, self.actual))
        ]


def read_evm(book, sheet_name: str) -> EvmSheet:
    grid = SheetGrid(require_sheet(book, sheet_name))
    header_row, period_columns = _period_header(grid)
    unit_column = grid.headers(header_row).get("unidad")
    series_by_label = {
        label: _preferred_series(grid, header_row, period_columns, unit_column, label)
        for label in (PLANNED_LABEL, EARNED_LABEL, ACTUAL_LABEL)
    }
    if series_by_label[PLANNED_LABEL] is None:
        raise LayoutChanged(f"No planned value row in {sheet_name!r}")
    return EvmSheet(
        title=sheet_name,
        periods=_periods_in_use(period_columns, series_by_label.values()),
        period_columns=period_columns,
        planned=series_by_label[PLANNED_LABEL],
        earned=series_by_label[EARNED_LABEL],
        actual=series_by_label[ACTUAL_LABEL],
    )


def read_original_plan_curve(book, sheet_name: str) -> dict[int, float]:
    """Cumulative USD of the superseded first baseline, which the Steering curve keeps as a reference line."""
    grid = SheetGrid(require_sheet(book, sheet_name))
    _, period_columns = _period_header(grid)
    try:
        label = grid.require_starting_with(ORIGINAL_PLAN_LABEL)
    except LayoutChanged:
        return {}
    return {
        period: number
        for period, column in period_columns.items()
        if (number := as_number(grid.value(label.row, column))) is not None
    }


def _periods_in_use(period_columns: dict[int, int], all_series) -> tuple[int, ...]:
    """Templates carry spare period columns (the cátedra's goes to 24); a period counts once any series uses it."""
    used = {
        period
        for series in all_series
        if series is not None
        for period, value in series.values.items()
        if value != 0
    }
    return tuple(period for period in sorted(period_columns) if period <= max(used, default=0))


def _period_header(grid: SheetGrid) -> tuple[int, dict[int, int]]:
    for row in range(1, grid.last_row + 1):
        period_columns = {}
        for column in range(1, grid.last_column + 1):
            match = PERIOD_HEADER.match(comparable_text(grid.value(row, column)))
            if match:
                period_columns[int(match["number"])] = column
        if len(period_columns) >= MINIMUM_PERIOD_COLUMNS:
            return row, period_columns
    raise LayoutChanged(f"No period header row (P1, P2... or Periodo 1...) in {grid.sheet.title!r}")


def _preferred_series(grid, header_row, period_columns, unit_column, label) -> EvmSeries | None:
    candidates = [
        _series_at(grid, row, period_columns, unit_column)
        for row in range(header_row + 1, grid.last_row + 1)
        if _is_per_period_row(grid.value(row, 1), label)
    ]
    in_hours = [series for series in candidates if series.unit == PREFERRED_UNIT]
    return (in_hours or candidates or [None])[0]


def _is_per_period_row(label_cell, label: str) -> bool:
    text = comparable_text(label_cell)
    return text.startswith(label) and "acumulado" not in text


def _series_at(grid, row, period_columns, unit_column) -> EvmSeries:
    values = {}
    for period, column in period_columns.items():
        number = as_number(grid.value(row, column))
        if number is not None:
            values[period] = number
    unit = comparable_text(grid.value(row, unit_column)) if unit_column else "as in the sheet"
    return EvmSeries(label=grid.text(row, 1), row=row, unit=unit, values=values)
