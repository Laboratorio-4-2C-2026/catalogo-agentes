import math
from dataclasses import dataclass
from datetime import date, timedelta

from .project import Calendar, Milestone

DAYS_PER_WEEK = 7


@dataclass(frozen=True)
class WeekPosition:
    as_of: date
    tablero_week: int
    tablero_week_monday: date
    project_week: int
    evm_period: int
    last_closed_evm_period: int
    todo_week: int
    todo_week_starts: date
    sprint_name: str | None
    upcoming_milestones: tuple[Milestone, ...]


def position_on(as_of: date, calendar: Calendar) -> WeekPosition:
    tablero_week = _week_number(as_of, calendar.tablero_week_one_monday)
    todo_week = _week_number(as_of, calendar.todo_week_one_starts)
    evm_period = evm_period_containing(as_of, calendar)
    return WeekPosition(
        as_of=as_of,
        tablero_week=tablero_week,
        tablero_week_monday=_week_start(calendar.tablero_week_one_monday, tablero_week),
        project_week=_week_number(as_of, calendar.project_week_one_starts),
        evm_period=evm_period,
        last_closed_evm_period=evm_period - 1,
        todo_week=todo_week,
        todo_week_starts=_week_start(calendar.todo_week_one_starts, todo_week),
        sprint_name=_sprint_on(as_of, calendar),
        upcoming_milestones=tuple(milestone for milestone in calendar.milestones if milestone.day >= as_of),
    )


def evm_period_containing(day: date, calendar: Calendar) -> int:
    """EVM periods run Friday to Thursday, so period N ends on the Thursday that closes project week N."""
    return math.ceil((day - calendar.project_week_one_starts).days / DAYS_PER_WEEK)


def evm_period_dates(period: int, calendar: Calendar) -> tuple[date, date]:
    period_end = calendar.project_week_one_starts + timedelta(days=DAYS_PER_WEEK * period)
    return period_end - timedelta(days=DAYS_PER_WEEK - 1), period_end


def _week_number(day: date, week_one_starts: date) -> int:
    return (day - week_one_starts).days // DAYS_PER_WEEK + 1


def _week_start(week_one_starts: date, week_number: int) -> date:
    return week_one_starts + timedelta(days=DAYS_PER_WEEK * (week_number - 1))


def _sprint_on(day: date, calendar: Calendar) -> str | None:
    for sprint in calendar.sprints:
        if sprint.starts <= day < sprint.ends:
            return sprint.name
    return None
