import json
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .shell import CommandFailed, CommandRunner, run_command

PULL_REQUEST_FIELDS = "number,title,headRefName,state,author,createdAt,mergedAt,url"
WORKFLOW_RUN_FIELDS = "databaseId,status,conclusion,event,createdAt,url"
COMPLETED = "completed"
SUCCESS = "success"


@dataclass(frozen=True)
class WorkflowRun:
    run_id: int
    status: str
    conclusion: str
    event: str
    created_at: datetime
    url: str

    @property
    def is_finished(self) -> bool:
        return self.status == COMPLETED

    @property
    def succeeded(self) -> bool:
        return self.is_finished and self.conclusion == SUCCESS


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    branch: str
    state: str
    author: str
    created_at: datetime
    merged_at: datetime | None
    url: str

    def issue_numbers(self, issue_key_pattern: re.Pattern) -> list[int]:
        return sorted({int(number) for number in issue_key_pattern.findall(f"{self.title} {self.branch}")})


def issue_key_pattern(team_key: str) -> re.Pattern:
    """Matches the team's issue key in a PR title or branch name, in any case; captures the number."""
    return re.compile(rf"\b{re.escape(team_key)}-(\d+)\b", re.IGNORECASE)


def list_pull_requests(repository: str, *, limit: int, run: CommandRunner = run_command) -> list[PullRequest]:
    output = run([
        "gh", "pr", "list",
        "--repo", repository,
        "--state", "all",
        "--limit", str(limit),
        "--json", PULL_REQUEST_FIELDS,
    ])
    return [pull_request_from(raw) for raw in json.loads(output.stdout)]


def list_workflow_runs(repository: str, workflow: str, *, limit: int, run: CommandRunner = run_command) -> list[WorkflowRun]:
    output = run([
        "gh", "run", "list",
        "--repo", repository,
        "--workflow", workflow,
        "--limit", str(limit),
        "--json", WORKFLOW_RUN_FIELDS,
    ])
    return [_workflow_run_from(raw) for raw in json.loads(output.stdout)]


def workflow_definition(repository: str, workflow: str, *, run: CommandRunner = run_command) -> str:
    listing = json.loads(run(["gh", "api", f"repos/{repository}/actions/workflows"]).stdout)
    paths = [entry["path"] for entry in listing["workflows"] if entry["name"] == workflow]
    if not paths:
        raise CommandFailed(["gh", "api", f"repos/{repository}/actions/workflows"], f"no workflow named {workflow!r}")
    return run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{repository}/contents/{paths[0]}"]).stdout


def run_artifact_texts(repository: str, run_id: int, *, run: CommandRunner = run_command) -> list[str]:
    """`gh run download` only writes to disk, so the artifacts land in a temporary folder outside the vault and are read back."""
    with tempfile.TemporaryDirectory(prefix="pm-weekly-artifacts-") as folder:
        try:
            run(["gh", "run", "download", str(run_id), "--repo", repository, "--dir", folder])
        except CommandFailed:
            return []
        return [path.read_text(encoding="utf-8") for path in sorted(Path(folder).rglob("*.json"))]


def raw_file(repository: str, path: str, *, ref: str, run: CommandRunner = run_command) -> str:
    output = run([
        "gh", "api",
        "-H", "Accept: application/vnd.github.raw",
        f"repos/{repository}/contents/{path}?ref={ref}",
    ])
    return output.stdout


def directory_entries(repository: str, path: str, *, ref: str, run: CommandRunner = run_command) -> list[str]:
    output = run(["gh", "api", f"repos/{repository}/contents/{path}?ref={ref}"])
    return [entry["name"] for entry in json.loads(output.stdout)]


def _workflow_run_from(raw: dict) -> WorkflowRun:
    return WorkflowRun(
        run_id=raw["databaseId"],
        status=raw["status"],
        conclusion=raw.get("conclusion") or "",
        event=raw["event"],
        created_at=datetime.fromisoformat(raw["createdAt"]),
        url=raw["url"],
    )


def pull_request_from(raw: dict) -> PullRequest:
    return PullRequest(
        number=raw["number"],
        title=raw["title"],
        branch=raw["headRefName"],
        state=raw["state"],
        author=(raw.get("author") or {}).get("login", ""),
        created_at=datetime.fromisoformat(raw["createdAt"]),
        merged_at=datetime.fromisoformat(raw["mergedAt"]) if raw.get("mergedAt") else None,
        url=raw["url"],
    )
