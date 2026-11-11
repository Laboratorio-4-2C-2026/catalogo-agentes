import json
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum
from zoneinfo import ZoneInfo

from .github import WorkflowRun
from .kpis import PRODUCTION, DayCompliance

SCHEDULED_EVENT = "schedule"
REPORT_COMMAND = "report"
DAYS_OF_SCHEDULE_HISTORY = 7
DAILY_CRON = re.compile(
    r"""
    cron: \s* ['"]?
    (?P<minute>\d{1,2}) \s+
    (?P<hour>\d{1,2}) \s+
    \* \s+ \* \s+ \*            # every day of every month, any weekday
    """,
    re.VERBOSE,
)


class DayState(Enum):
    COMPLETE = "complete"
    SENT = "sent and accepted, not yet on the data branch"
    RUNNING = "a run is in progress"
    WAITING = "waiting for the scheduled run"
    AT_RISK = "at risk"
    INCOMPLETE = "incomplete"
    LOST = "lost"


@dataclass(frozen=True)
class ReportSchedule:
    """The workflow's cron times, plus how late GitHub actually started them in the last week."""

    utc_times: tuple[time, ...]
    longest_delay: timedelta

    def local_times(self, day: date, zone: ZoneInfo) -> list[time]:
        return [datetime.combine(day, utc_time, tzinfo=timezone.utc).astimezone(zone).time() for utc_time in self.utc_times]

    def pending_starts(self, now: datetime) -> list[datetime]:
        """Scheduled starts of today that may still show up, given the delays already seen."""
        starts = [datetime.combine(now.date(), local_time, tzinfo=now.tzinfo) for local_time in self.local_times(now.date(), now.tzinfo)]
        return [start for start in starts if now < start + self.longest_delay]


@dataclass(frozen=True)
class DeliveredReport:
    """What one run's artifact says it sent to the platform and how the platform answered."""

    run_id: int
    command: str
    kpi_ids: frozenset[str]
    platform_status: int | None

    @property
    def accepted(self) -> bool:
        return self.command == REPORT_COMMAND and self.platform_status is not None and 200 <= self.platform_status < 300


@dataclass(frozen=True)
class DayWatch:
    day: date
    state: DayState
    compliance: DayCompliance | None
    runs: tuple[WorkflowRun, ...]
    accepted_kpis: frozenset[str]

    @property
    def failed_runs(self) -> tuple[WorkflowRun, ...]:
        return tuple(run for run in self.runs if run.is_finished and not run.succeeded)

    @property
    def kpis_not_accepted(self) -> list[str]:
        expected = self.compliance.expected_kpis if self.compliance else frozenset()
        return sorted(expected - self.accepted_kpis)


def report_schedule(workflow_definition: str, runs: list[WorkflowRun], *, today: date) -> ReportSchedule:
    utc_times = tuple(
        time(int(match["hour"]), int(match["minute"])) for match in DAILY_CRON.finditer(workflow_definition)
    )
    return ReportSchedule(utc_times, _longest_delay(runs, utc_times, today=today))


def delivered_report(run_id: int, artifact_text: str) -> DeliveredReport:
    artifact = json.loads(artifact_text)
    return DeliveredReport(
        run_id=run_id,
        command=artifact.get("command", ""),
        kpi_ids=frozenset(row["kpi_id"] for row in artifact.get("sentBody") or [] if row.get("env") == PRODUCTION),
        platform_status=(artifact.get("platformResponse") or {}).get("status"),
    )


def runs_on(day: date, runs: list[WorkflowRun], zone: ZoneInfo) -> tuple[WorkflowRun, ...]:
    return tuple(sorted(
        (run for run in runs if run.created_at.astimezone(zone).date() == day),
        key=lambda run: run.created_at,
    ))


def watch_open_day(
    compliance: DayCompliance | None,
    runs_of_the_day: tuple[WorkflowRun, ...],
    deliveries: list[DeliveredReport],
    *,
    now: datetime,
    schedule: ReportSchedule,
) -> DayWatch:
    """A day still receiving values: the artifacts say what the platform accepted, before the data branch shows it."""
    accepted = _accepted_kpis(deliveries)
    if compliance and compliance.is_complete:
        state = DayState.COMPLETE
    elif compliance and compliance.expected_kpis <= accepted:
        state = DayState.SENT
    elif any(not run.is_finished for run in runs_of_the_day):
        state = DayState.RUNNING
    elif not runs_of_the_day and schedule.pending_starts(now):
        state = DayState.WAITING
    else:
        state = DayState.AT_RISK
    return DayWatch(now.date(), state, compliance, runs_of_the_day, accepted)


def watch_closed_day(
    compliance: DayCompliance | None,
    runs_of_the_day: tuple[WorkflowRun, ...],
    deliveries: list[DeliveredReport],
    *,
    day: date,
) -> DayWatch:
    """A closed day is graded on what the platform received; accepted artifacts alone mean the data branch lags."""
    accepted = _accepted_kpis(deliveries)
    if compliance and compliance.is_complete:
        state = DayState.COMPLETE
    elif compliance and compliance.received_kpis:
        state = DayState.INCOMPLETE
    elif compliance and compliance.expected_kpis <= accepted:
        state = DayState.SENT
    elif accepted:
        state = DayState.INCOMPLETE
    else:
        state = DayState.LOST
    return DayWatch(day, state, compliance, runs_of_the_day, accepted)


def _accepted_kpis(deliveries: list[DeliveredReport]) -> frozenset[str]:
    return frozenset(kpi_id for delivery in deliveries if delivery.accepted for kpi_id in delivery.kpi_ids)


def _longest_delay(runs: list[WorkflowRun], utc_times: tuple[time, ...], *, today: date) -> timedelta:
    since = today - timedelta(days=DAYS_OF_SCHEDULE_HISTORY)
    delays = [
        _delay_after_cron(run.created_at.astimezone(timezone.utc), utc_times)
        for run in runs
        if run.event == SCHEDULED_EVENT and run.created_at.date() >= since
    ]
    return max((delay for delay in delays if delay is not None), default=timedelta(0))


def _delay_after_cron(started: datetime, utc_times: tuple[time, ...]) -> timedelta | None:
    """A run late enough crosses midnight UTC, so the cron times of the day before are candidates too."""
    candidates = [
        datetime.combine(started.date() - timedelta(days=days_back), utc_time, tzinfo=timezone.utc)
        for days_back in (0, 1)
        for utc_time in utc_times
    ]
    earlier = [candidate for candidate in candidates if candidate <= started]
    return started - max(earlier) if earlier else None
