from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .open_pull_requests import APPROVED, CHANGES_REQUESTED, CheckOutcome, OpenPullRequest


class Waiting(Enum):
    ON_MERGE = "approved, waiting for a merge"
    ON_AUTHOR = "changes requested, waiting for the author"
    ON_REVIEW = "waiting for a review"
    ON_RE_REVIEW = "changes pushed, waiting for a new review"


# 48 h is the review threshold of the cátedra's blocker detector. An approved PR has nothing left
# but the merge, and only a merge earns value, so it gets a single day.
WAIT_LIMITS = {
    Waiting.ON_MERGE: timedelta(hours=24),
    Waiting.ON_AUTHOR: timedelta(hours=48),
    Waiting.ON_REVIEW: timedelta(hours=48),
    Waiting.ON_RE_REVIEW: timedelta(hours=48),
}


@dataclass(frozen=True)
class Wait:
    kind: Waiting
    since: datetime

    def age_at(self, now: datetime) -> timedelta:
        return now - self.since

    def is_over_limit_at(self, now: datetime) -> bool:
        return self.age_at(now) > WAIT_LIMITS[self.kind]


@dataclass(frozen=True)
class WaitingPullRequest:
    pull_request: OpenPullRequest
    wait: Wait


@dataclass(frozen=True)
class StackedPullRequest:
    pull_request: OpenPullRequest
    base_pull_request: OpenPullRequest | None


@dataclass(frozen=True)
class ReviewQueue:
    waiting: tuple[WaitingPullRequest, ...]
    drafts: tuple[OpenPullRequest, ...]
    stacked: tuple[StackedPullRequest, ...]
    with_conflicts: tuple[OpenPullRequest, ...]
    with_failing_checks: tuple[OpenPullRequest, ...]

    @property
    def open_count(self) -> int:
        return len(self.waiting) + len(self.drafts)


def review_queue_of(pull_requests: list[OpenPullRequest], *, default_branch: str) -> ReviewQueue:
    ready_for_review = [pull_request for pull_request in pull_requests if not pull_request.is_draft]
    return ReviewQueue(
        waiting=tuple(WaitingPullRequest(pull_request, current_wait(pull_request)) for pull_request in ready_for_review),
        drafts=tuple(pull_request for pull_request in pull_requests if pull_request.is_draft),
        stacked=_stacked(pull_requests, default_branch=default_branch),
        with_conflicts=tuple(pull_request for pull_request in ready_for_review if pull_request.has_conflicts),
        with_failing_checks=tuple(
            pull_request for pull_request in ready_for_review if pull_request.checks == CheckOutcome.FAILING
        ),
    )


def current_wait(pull_request: OpenPullRequest) -> Wait:
    decision = _review_decision(pull_request)
    if decision == APPROVED:
        return Wait(Waiting.ON_MERGE, since=_latest_review_at(pull_request, APPROVED))
    if decision == CHANGES_REQUESTED:
        return _wait_after_change_request(pull_request)
    return Wait(Waiting.ON_REVIEW, since=pull_request.last_activity_at)


def _review_decision(pull_request: OpenPullRequest) -> str:
    """GitHub computes a decision only when the base branch requires reviews; without that rule the latest reviews decide."""
    if pull_request.review_decision:
        return pull_request.review_decision
    states = {review.state for review in pull_request.latest_reviews}
    if CHANGES_REQUESTED in states:
        return CHANGES_REQUESTED
    if APPROVED in states:
        return APPROVED
    return ""


def _wait_after_change_request(pull_request: OpenPullRequest) -> Wait:
    requested_at = _latest_review_at(pull_request, CHANGES_REQUESTED)
    if pull_request.last_commit_at > requested_at:
        return Wait(Waiting.ON_RE_REVIEW, since=pull_request.last_commit_at)
    return Wait(Waiting.ON_AUTHOR, since=requested_at)


def _latest_review_at(pull_request: OpenPullRequest, state: str) -> datetime:
    """Falls back to the last activity when GitHub reports a decision whose review is not among the latest ones."""
    moments = [review.submitted_at for review in pull_request.latest_reviews if review.state == state]
    return max(moments, default=pull_request.last_activity_at)


def _stacked(pull_requests: list[OpenPullRequest], *, default_branch: str) -> tuple[StackedPullRequest, ...]:
    open_by_head_branch = {pull_request.head_branch: pull_request for pull_request in pull_requests}
    return tuple(
        StackedPullRequest(pull_request, base_pull_request=open_by_head_branch.get(pull_request.base_branch))
        for pull_request in pull_requests
        if pull_request.base_branch != default_branch
    )
