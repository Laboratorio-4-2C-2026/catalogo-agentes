from dataclasses import dataclass
from datetime import datetime, timedelta

from ..kpi_watch import DayState, DayWatch, ReportSchedule


@dataclass(frozen=True)
class WatchedWorkflow:
    name: str
    repository: str
    compliance_url: str


def print_kpi_watch(
    open_day: DayWatch | None,
    closed_days: list[DayWatch],
    *,
    now: datetime,
    schedule: ReportSchedule,
    workflow: WatchedWorkflow,
) -> None:
    print(f"KPI watch · {now:%a %d/%m %H:%M} ({now.tzinfo}) · workflow {workflow.name!r} in {workflow.repository}")
    print(
        f"Scheduled at {_listed(schedule.local_times(now.date(), now.tzinfo))} by the workflow's cron; "
        f"GitHub started them up to {_duration(schedule.longest_delay)} late in the last 7 days"
    )
    if open_day:
        print()
        _print_day(open_day, heading="Today ", now=now, schedule=schedule, workflow=workflow)
    if closed_days:
        print()
        print("Closed days")
        for watch in closed_days:
            _print_day(watch, heading="", now=now, schedule=schedule, workflow=workflow)


def _print_day(watch: DayWatch, *, heading: str, now: datetime, schedule: ReportSchedule, workflow: WatchedWorkflow) -> None:
    print(f"{heading}{watch.day:%a %d/%m}: {watch.state.value.upper()}{_received(watch)}{_accepted(watch)}")
    for run in watch.runs:
        outcome = run.conclusion or run.status
        print(f"  run {run.created_at.astimezone(now.tzinfo):%H:%M}  {run.event:<17} {outcome:<11} {run.url}")
    advice = _advice(watch, now=now, schedule=schedule, workflow=workflow)
    if advice:
        print(f"  -> {advice}")


def _received(watch: DayWatch) -> str:
    compliance = watch.compliance
    if compliance is None:
        return ""
    return f" · data branch {len(compliance.received_kpis)}/{len(compliance.expected_kpis)}, grade {compliance.grade}"


def _accepted(watch: DayWatch) -> str:
    if watch.state == DayState.COMPLETE:
        return ""
    expected = len(watch.compliance.expected_kpis) if watch.compliance else 0
    return f" · accepted by the platform per the run artifacts {len(watch.accepted_kpis)}/{expected}"


def _advice(watch: DayWatch, *, now: datetime, schedule: ReportSchedule, workflow: WatchedWorkflow) -> str:
    match watch.state:
        case DayState.COMPLETE:
            return ""
        case DayState.SENT:
            return f"Nothing to do: the platform accepted every KPI. Confirm tomorrow, or now on {workflow.compliance_url}"
        case DayState.RUNNING:
            return "A run is in progress; check again when it finishes."
        case DayState.WAITING:
            return _waiting_advice(now, schedule)
        case DayState.AT_RISK:
            return _at_risk_advice(watch, now=now, schedule=schedule, workflow=workflow)
        case DayState.INCOMPLETE:
            return f"The day closed without {_missing(watch)}: register it as an incident in the Tablero."
        case DayState.LOST:
            return "Nothing arrived and the day is closed, so it is lost for good: register it as an incident in the Tablero."


def _waiting_advice(now: datetime, schedule: ReportSchedule) -> str:
    next_start = schedule.pending_starts(now)[0]
    deadline = next_start + schedule.longest_delay
    return (
        f"No run yet today. The next one is scheduled at {next_start:%H:%M} and has started as late as {deadline:%H:%M}; "
        "check again after that."
    )


def _at_risk_advice(watch: DayWatch, *, now: datetime, schedule: ReportSchedule, workflow: WatchedWorkflow) -> str:
    sentences = [f"Not accepted yet: {_missing(watch)}."]
    if watch.failed_runs:
        last_failure = watch.failed_runs[-1]
        sentences.append(f"Why the last run failed: gh run view {last_failure.run_id} --repo {workflow.repository} --log-failed")
    pending = schedule.pending_starts(now)
    if pending:
        sentences.append(
            f"The run scheduled at {pending[0]:%H:%M} may still save the day, but a configuration error fails it the same way."
        )
    sentences.append(
        f"Before midnight, ask someone with write access to {workflow.repository} to run {workflow.name!r} by hand "
        f"(Actions > {workflow.name} > Run workflow, command report, dry run off)."
    )
    return " ".join(sentences)


def _missing(watch: DayWatch) -> str:
    return ", ".join(watch.kpis_not_accepted) or "some KPIs"


def _listed(run_times) -> str:
    return " and ".join(f"{run_time:%H:%M}" for run_time in run_times) or "(no daily cron found)"


def _duration(delay: timedelta) -> str:
    hours, seconds = divmod(int(delay.total_seconds()), 3600)
    return f"{hours}h{seconds // 60:02d}"
