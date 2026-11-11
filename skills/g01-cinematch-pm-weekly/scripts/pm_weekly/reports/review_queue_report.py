import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from ..review_queue.blockers import WAIT_LIMITS, ReviewQueue, StackedPullRequest, Waiting, WaitingPullRequest
from ..review_queue.open_pull_requests import OpenPullRequest

WHO_HAS_TO_ACT = (
    ("Waiting on a merge", (Waiting.ON_MERGE,)),
    ("Waiting on the author", (Waiting.ON_AUTHOR,)),
    ("Waiting on a reviewer", (Waiting.ON_REVIEW, Waiting.ON_RE_REVIEW)),
)
OVER_LIMIT_MARKER = "OVER"


@dataclass(frozen=True)
class RepositoryContext:
    repository: str
    default_branch: str
    issue_key_pattern: re.Pattern
    team_key: str


def print_review_queue(queue: ReviewQueue, *, now: datetime, context: RepositoryContext) -> None:
    print(f"Review queue · {now:%a %d/%m %H:%M} ({now.tzinfo}) · {context.repository}, {queue.open_count} open PRs")
    print(f"Limits: {_limits()}")
    if not queue.open_count:
        print("No open pull requests.")
        return
    for heading, kinds in WHO_HAS_TO_ACT:
        entries = [entry for entry in queue.waiting if entry.wait.kind in kinds]
        _print_section(heading, [_waiting_line(entry, now=now, context=context) for entry in _oldest_first(entries)])
    _print_section("Before merging", _before_merging_lines(queue, context))
    _print_section("Drafts, not chased", [_draft_line(draft, now=now, context=context) for draft in queue.drafts])


def _print_section(heading: str, lines: list[str]) -> None:
    if not lines:
        return
    print()
    print(heading)
    for line in lines:
        print(f"  {line}")


def _oldest_first(entries: list[WaitingPullRequest]) -> list[WaitingPullRequest]:
    return sorted(entries, key=lambda entry: entry.wait.since)


def _waiting_line(entry: WaitingPullRequest, *, now: datetime, context: RepositoryContext) -> str:
    marker = OVER_LIMIT_MARKER if entry.wait.is_over_limit_at(now) else " " * len(OVER_LIMIT_MARKER)
    since = entry.wait.since.astimezone(now.tzinfo)
    state = f"{entry.wait.kind.value} since {since:%d/%m %H:%M} ({_age(entry.wait.age_at(now))})"
    return f"{marker}  {_numbered(entry.pull_request, context)}  {state}  {_authored(entry.pull_request)}"


def _before_merging_lines(queue: ReviewQueue, context: RepositoryContext) -> list[str]:
    return [
        *(_stacked_line(stacked, context) for stacked in queue.stacked),
        *(f"#{conflicted.pull_request.number} has merge conflicts with {conflicted.base_branch}" for conflicted in queue.with_conflicts),
        *(f"#{failing.pull_request.number} has failing checks on its last commit" for failing in queue.with_failing_checks),
    ]


def _stacked_line(stacked: StackedPullRequest, context: RepositoryContext) -> str:
    number = stacked.pull_request.pull_request.number
    base_branch = stacked.pull_request.base_branch
    if stacked.base_pull_request is None:
        return f"#{number} targets {base_branch}, which has no open PR: retarget it to {context.default_branch} before merging"
    base_number = stacked.base_pull_request.pull_request.number
    return (
        f"#{number} targets {base_branch}, the branch of #{base_number}: merge #{base_number} first, "
        f"then retarget #{number} to {context.default_branch} and merge it"
    )


def _draft_line(draft: OpenPullRequest, *, now: datetime, context: RepositoryContext) -> str:
    last_commit = draft.last_commit_at.astimezone(now.tzinfo)
    return f"{_numbered(draft, context)}  last commit {last_commit:%d/%m}  {_authored(draft)}"


def _numbered(open_pull_request: OpenPullRequest, context: RepositoryContext) -> str:
    return f"#{open_pull_request.pull_request.number} {_issue_keys(open_pull_request, context)}"


def _authored(open_pull_request: OpenPullRequest) -> str:
    pull_request = open_pull_request.pull_request
    return f"by {pull_request.author}: {pull_request.title}"


def _issue_keys(open_pull_request: OpenPullRequest, context: RepositoryContext) -> str:
    numbers = open_pull_request.pull_request.issue_numbers(context.issue_key_pattern)
    return ", ".join(f"{context.team_key}-{number}" for number in numbers) or f"(no {context.team_key} key)"


def _limits() -> str:
    return "; ".join(f"{kind.value} {_whole_hours(limit)}h" for kind, limit in WAIT_LIMITS.items())


def _whole_hours(limit: timedelta) -> int:
    return int(limit.total_seconds() // 3600)


def _age(elapsed: timedelta) -> str:
    days, seconds = divmod(int(elapsed.total_seconds()), 86400)
    hours = seconds // 3600
    return f"{days}d {hours}h" if days else f"{hours}h"
