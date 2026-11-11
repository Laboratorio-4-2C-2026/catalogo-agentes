import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ..github import PULL_REQUEST_FIELDS, PullRequest, pull_request_from
from ..shell import CommandRunner, run_command

REVIEW_FIELDS = "baseRefName,isDraft,reviewDecision,latestReviews,commits,mergeable,statusCheckRollup"
APPROVED = "APPROVED"
CHANGES_REQUESTED = "CHANGES_REQUESTED"
CONFLICTING = "CONFLICTING"
COMPLETED_CHECK_RUN = "COMPLETED"
COMMIT_STATUS = "StatusContext"
FAILED_CHECK_RUN_CONCLUSIONS = frozenset({"FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED", "STARTUP_FAILURE"})
FAILED_COMMIT_STATUS_STATES = frozenset({"FAILURE", "ERROR"})
PENDING_COMMIT_STATUS_STATES = frozenset({"PENDING", "EXPECTED"})


class CheckOutcome(Enum):
    PASSING = "passing"
    FAILING = "failing"
    PENDING = "pending"
    NONE = "no checks"


@dataclass(frozen=True)
class Review:
    reviewer: str
    state: str
    submitted_at: datetime


@dataclass(frozen=True)
class OpenPullRequest:
    pull_request: PullRequest
    base_branch: str
    is_draft: bool
    review_decision: str
    latest_reviews: tuple[Review, ...]
    last_commit_at: datetime
    has_conflicts: bool
    checks: CheckOutcome

    @property
    def head_branch(self) -> str:
        return self.pull_request.branch

    @property
    def last_activity_at(self) -> datetime:
        return max(self.pull_request.created_at, self.last_commit_at)


def list_open_pull_requests(repository: str, *, limit: int, run: CommandRunner = run_command) -> list[OpenPullRequest]:
    output = run([
        "gh", "pr", "list",
        "--repo", repository,
        "--state", "open",
        "--limit", str(limit),
        "--json", f"{PULL_REQUEST_FIELDS},{REVIEW_FIELDS}",
    ])
    return [_open_pull_request_from(raw) for raw in json.loads(output.stdout)]


def _open_pull_request_from(raw: dict) -> OpenPullRequest:
    pull_request = pull_request_from(raw)
    return OpenPullRequest(
        pull_request=pull_request,
        base_branch=raw["baseRefName"],
        is_draft=raw["isDraft"],
        review_decision=raw.get("reviewDecision") or "",
        latest_reviews=tuple(_review_from(review) for review in raw.get("latestReviews") or [] if review.get("submittedAt")),
        last_commit_at=_last_commit_at(raw.get("commits") or [], default=pull_request.created_at),
        has_conflicts=raw.get("mergeable") == CONFLICTING,
        checks=_check_outcome(raw.get("statusCheckRollup") or []),
    )


def _review_from(raw: dict) -> Review:
    return Review(
        reviewer=(raw.get("author") or {}).get("login", ""),
        state=raw["state"],
        submitted_at=datetime.fromisoformat(raw["submittedAt"]),
    )


def _last_commit_at(commits: list[dict], *, default: datetime) -> datetime:
    return max((datetime.fromisoformat(commit["committedDate"]) for commit in commits), default=default)


def _check_outcome(rollup: list[dict]) -> CheckOutcome:
    if not rollup:
        return CheckOutcome.NONE
    if any(_check_failed(check) for check in rollup):
        return CheckOutcome.FAILING
    if any(_check_pending(check) for check in rollup):
        return CheckOutcome.PENDING
    return CheckOutcome.PASSING


def _check_failed(check: dict) -> bool:
    return check.get("conclusion") in FAILED_CHECK_RUN_CONCLUSIONS or check.get("state") in FAILED_COMMIT_STATUS_STATES


def _check_pending(check: dict) -> bool:
    """The rollup mixes Actions check runs, which carry a status, with legacy commit statuses, which carry only a state."""
    if check.get("__typename") == COMMIT_STATUS:
        return check.get("state") in PENDING_COMMIT_STATUS_STATES
    return check.get("status") != COMPLETED_CHECK_RUN
