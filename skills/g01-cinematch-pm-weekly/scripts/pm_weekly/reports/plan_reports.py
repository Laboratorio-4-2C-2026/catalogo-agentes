from ..project import Calendar
from ..schedule import WeekPosition, evm_period_dates
from ..spreadsheets.budget import EvmSettings
from ..spreadsheets.evm import PREFERRED_UNIT, EvmSheet
from ..spreadsheets.gantt import GanttTask
from ..spreadsheets.workbook import cell_reference


def print_calendar(position: WeekPosition, calendar: Calendar) -> None:
    period_start, period_end = evm_period_dates(position.evm_period, calendar)
    closed_start, closed_end = evm_period_dates(position.last_closed_evm_period, calendar)
    print(f"As of {position.as_of:%a %d/%m/%Y} · {position.sprint_name or 'outside the sprints'}")
    print(f"  Tablero column:  Sem-{position.tablero_week:02d} (report date {position.tablero_week_monday:%d/%m})")
    print(f"  TODO section:    Semana {position.todo_week} ({position.todo_week_starts:%d/%m})")
    print(f"  Gantt week:      W{position.project_week}")
    print(f"  EVM period:      P{position.evm_period} ({period_start:%d/%m} to {period_end:%d/%m}), in progress")
    print(f"  Last closed EVM: P{position.last_closed_evm_period} ({closed_start:%d/%m} to {closed_end:%d/%m})")
    print("Upcoming:")
    for milestone in position.upcoming_milestones:
        print(f"  {milestone.day:%d/%m} {milestone.name} (in {(milestone.day - position.as_of).days} days)")


def print_evm(sheet: EvmSheet, last_closed_period: int, settings: EvmSettings | None) -> None:
    print(f"Sheet {sheet.title!r} · BAC {sheet.budget_at_completion:.1f} ({sheet.planned.unit})")
    print("Period".ljust(8) + "PV".rjust(10) + "EV".rjust(10) + "AC".rjust(10))
    for period in sheet.periods:
        cells = [_value_in(series, period) for series in (sheet.planned, sheet.earned, sheet.actual)]
        print(f"P{period}".ljust(8) + "".join(cell.rjust(10) for cell in cells))
    _print_indices(sheet)
    missing = sheet.periods_missing_until(last_closed_period)
    if missing:
        print(f"MISSING: EV or AC not loaded for {', '.join(f'P{period}' for period in missing)} (last closed: P{last_closed_period})")
        _print_input_cells(sheet, missing)
    if settings:
        _print_cut(sheet, settings)


def _print_input_cells(sheet: EvmSheet, periods: list[int]) -> None:
    if sheet.earned is None or sheet.actual is None:
        return
    unit = "HH" if sheet.earned.unit == PREFERRED_UNIT else "the sheet's own unit"
    for period in periods:
        print(f"  P{period}: EV in {sheet.input_cell(sheet.earned, period)}, AC in {sheet.input_cell(sheet.actual, period)}, in {unit}")


def _print_cut(sheet: EvmSheet, settings: EvmSettings) -> None:
    cut = settings.measurement_cut
    reference = cell_reference(settings.sheet_title, cut.cell)
    loaded = sheet.last_loaded_period
    if loaded is not None and cut.value == loaded:
        print(f"Cut {reference} = {cut.value:g}, the last period with EV and AC")
        return
    print(
        f"MISMATCH: the cut {reference} is {cut.value:g} but the last period with EV and AC is P{loaded}. "
        f"Set it to {loaded}: the USD rows, indices and curves stop at the cut"
    )


def _print_indices(sheet: EvmSheet) -> None:
    last_earned = sheet.earned.last_period() if sheet.earned else None
    last_actual = sheet.actual.last_period() if sheet.actual else None
    if last_earned is None or last_actual is None:
        print("No earned value or actual cost loaded: SPI and CPI cannot be computed.")
        return
    cut = min(last_earned, last_actual)
    planned, earned, actual = (series.cumulative_until(cut) for series in (sheet.planned, sheet.earned, sheet.actual))
    print(
        f"Cut at P{cut}: PV {planned:.1f} · EV {earned:.1f} · AC {actual:.1f} · "
        f"SPI {earned / planned:.2f} · CPI {earned / actual:.2f} · "
        f"physical progress {earned / sheet.budget_at_completion:.1%} of BAC"
    )


def _value_in(series, period: int) -> str:
    if series is None or period not in series.values:
        return "-"
    return f"{series.values[period]:.1f}"


def print_gantt_tasks(tasks: tuple[GanttTask, ...]) -> None:
    for task in tasks:
        week = f"W{task.week}" if task.week else "-"
        points = "-" if task.points is None else f"{task.points:g}"
        print(f"{task.task_id.ljust(8)} {week.ljust(4)} {points.rjust(4)}  {task.epic.ljust(9)} {task.name}  {task.notes}")
    print(f"{len(tasks)} tasks, {sum(task.points or 0 for task in tasks):g} points")


def print_points(found: dict[str, GanttTask], outside_baseline: list[str]) -> None:
    for task_id, task in found.items():
        print(f"{task_id.ljust(8)} {task.points or 0:g} points  W{task.week}  {task.name}")
    print(f"Baseline points: {sum(task.points or 0 for task in found.values()):g}")
    if outside_baseline:
        print(
            f"Not in the gantt: {', '.join(outside_baseline)}. They earn no value unless a later baseline "
            "change added them, or they are the Linear number of a NEW-* placeholder (references/evm.md)"
        )
