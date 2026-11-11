import re
from datetime import date
from zoneinfo import ZoneInfo

from ..doctor import Check
from ..github import PullRequest
from ..kpis import DayCompliance, GradingWindow


def print_checks(checks: list[Check]) -> None:
    for check in checks:
        status = "OK     " if check.ready else "MISSING"
        fix = f"  -> {check.fix}" if check.fix else ""
        print(f"{status} {check.name.ljust(14)} {check.detail}{fix}")
    print("Linear is read through the Linear MCP inside Claude Code, which this script cannot check: see references/setup.md#linear")


def print_kpi_compliance(window: GradingWindow, days: list[DayCompliance], *, today: date) -> None:
    print(f"Grading window {window.starts_on:%d/%m} to {window.ends_on:%d/%m}, by reception day in {window.timezone}")
    for day in days:
        suffix = " (today, still open)" if day.day == today else ""
        missing = f" missing: {', '.join(day.missing_kpis)}" if day.missing_kpis else ""
        print(f"  {day.day:%a %d/%m}  grade {day.grade:>2}  received {len(day.received_kpis)}/{len(day.expected_kpis)} catalog{missing}{suffix}")
    closed_days = [day for day in days if day.day < today]
    if closed_days:
        average = sum(day.grade for day in closed_days) / len(closed_days)
        lost = [f"{day.day:%d/%m}" for day in closed_days if not day.received_kpis]
        print(f"Average over {len(closed_days)} closed days: {average:.2f}")
        if lost:
            print(f"Days with nothing received (lost for good): {', '.join(lost)}")


def print_pull_requests(
    pull_requests: list[PullRequest],
    *,
    issue_key_pattern: re.Pattern,
    team_key: str,
    zone: ZoneInfo,
) -> None:
    by_issue: dict[int, list[PullRequest]] = {}
    unlinked = []
    for pull_request in pull_requests:
        numbers = pull_request.issue_numbers(issue_key_pattern)
        if not numbers:
            unlinked.append(pull_request)
        for number in numbers:
            by_issue.setdefault(number, []).append(pull_request)
    for number in sorted(by_issue):
        print(f"{team_key}-{number}")
        for pull_request in by_issue[number]:
            print(f"  {_describe(pull_request, zone)}")
    if unlinked:
        print(f"Without a {team_key} key in title or branch:")
        for pull_request in unlinked:
            print(f"  {_describe(pull_request, zone)}")


def _describe(pull_request: PullRequest, zone: ZoneInfo) -> str:
    if pull_request.merged_at:
        status = f"merged {pull_request.merged_at.astimezone(zone):%d/%m %H:%M}"
    else:
        status = f"{pull_request.state.lower()}, opened {pull_request.created_at.astimezone(zone):%d/%m}"
    return f"#{pull_request.number} {status} by {pull_request.author}: {pull_request.title}"
