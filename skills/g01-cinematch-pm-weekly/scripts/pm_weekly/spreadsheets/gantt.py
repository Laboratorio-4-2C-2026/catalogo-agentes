import re
from dataclasses import dataclass

from .workbook import SheetGrid, as_number, column_starting_with, require_sheet

WEEK_HEADER = re.compile(r"^w(?P<number>\d+)$")


@dataclass(frozen=True)
class GanttTask:
    task_id: str
    name: str
    epic: str
    week: int | None
    points: float | None
    notes: str


def read_gantt(book, sheet_name: str) -> tuple[GanttTask, ...]:
    grid = SheetGrid(require_sheet(book, sheet_name))
    header = grid.require("Task ID")
    headers = grid.headers(header.row)
    week_columns = {
        int(match["number"]): column
        for text, column in headers.items()
        if (match := WEEK_HEADER.match(text))
    }
    columns = {
        name: column_starting_with(headers, name, sheet_title=sheet_name)
        for name in ("Task ID", "Task Name", "Epic", "Notas", "Puntos")
    }
    tasks = []
    for row in range(header.row + 1, grid.last_row + 1):
        if not grid.text(row, columns["Task ID"]):
            break
        tasks.append(_task_at(grid, row, columns, week_columns))
    return tuple(tasks)


def _task_at(grid: SheetGrid, row: int, columns: dict[str, int], week_columns: dict[int, int]) -> GanttTask:
    return GanttTask(
        task_id=grid.text(row, columns["Task ID"]).upper(),
        name=grid.text(row, columns["Task Name"]),
        epic=grid.text(row, columns["Epic"]),
        week=_marked_week(grid, row, week_columns),
        points=as_number(grid.value(row, columns["Puntos"])),
        notes=grid.text(row, columns["Notas"]),
    )


def _marked_week(grid: SheetGrid, row: int, week_columns: dict[int, int]) -> int | None:
    marked = [week for week, column in week_columns.items() if grid.text(row, column)]
    return marked[0] if marked else None


def points_for(tasks: tuple[GanttTask, ...], task_ids: list[str]) -> tuple[dict[str, GanttTask], list[str]]:
    by_id = {task.task_id: task for task in tasks}
    wanted = [task_id.strip().upper() for task_id in task_ids if task_id.strip()]
    found = {task_id: by_id[task_id] for task_id in wanted if task_id in by_id}
    outside_baseline = [task_id for task_id in wanted if task_id not in by_id]
    return found, outside_baseline
