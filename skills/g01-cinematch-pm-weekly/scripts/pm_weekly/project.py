import json
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

PROJECT_FILE = Path(__file__).resolve().parents[2] / "project.json"
DRIVE_FOLDER_VARIABLE = "CINEMATCH_DRIVE_FOLDER_ID"
KPI_PROJECT_VARIABLE = "CINEMATCH_KPI_PROJECT_ID"
SETTINGS_GUIDE = "references/setup.md#environment-variables"


class MissingSetting(Exception):
    pass


def setting_from_environment(variable: str) -> str:
    value = os.environ.get(variable, "").strip()
    if not value:
        raise MissingSetting(f"{variable} is not set; see {SETTINGS_GUIDE}")
    return value


@dataclass(frozen=True)
class Milestone:
    day: date
    name: str


@dataclass(frozen=True)
class Sprint:
    name: str
    starts: date
    ends: date


@dataclass(frozen=True)
class Calendar:
    project_week_one_starts: date
    todo_week_one_starts: date
    tablero_week_one_monday: date
    sprints: tuple[Sprint, ...]
    milestones: tuple[Milestone, ...]


@dataclass(frozen=True)
class Project:
    timezone: str
    drive_files: dict[str, str]
    tablero_tab: str
    evm_sheet: str
    evm_catedra_sheet: str
    evm_settings_sheet: str
    budget_sheet: str
    gantt_sheet: str
    app_repository: str
    app_default_branch: str
    kpi_workflow: str
    kpi_repository: str
    kpi_branch: str
    kpi_compliance_url: str
    linear_team_key: str
    calendar: Calendar

    def drive_file(self, key: str) -> str:
        return self.drive_files[key]

    @property
    def drive_folder_id(self) -> str:
        """Read on use, so commands that never touch Drive run without it."""
        return setting_from_environment(DRIVE_FOLDER_VARIABLE)

    @property
    def kpi_project_id(self) -> str:
        """Read on use, so commands that never touch the KPI platform run without it."""
        return setting_from_environment(KPI_PROJECT_VARIABLE)


def load_project(path: Path = PROJECT_FILE) -> Project:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Project(
        timezone=raw["timezone"],
        drive_files=dict(raw["drive"]["files"]),
        tablero_tab=raw["sheets"]["tablero_tab"],
        evm_sheet=raw["sheets"]["evm"],
        evm_catedra_sheet=raw["sheets"]["evm_catedra"],
        evm_settings_sheet=raw["sheets"]["evm_settings"],
        budget_sheet=raw["sheets"]["budget"],
        gantt_sheet=raw["sheets"]["gantt"],
        app_repository=raw["github"]["app_repository"],
        app_default_branch=raw["github"]["app_default_branch"],
        kpi_workflow=raw["github"]["kpi_workflow"],
        kpi_repository=raw["github"]["kpi_repository"],
        kpi_branch=raw["github"]["kpi_branch"],
        kpi_compliance_url=raw["kpi_compliance_url"],
        linear_team_key=raw["linear"]["team_key"],
        calendar=_calendar_from(raw["calendar"]),
    )


def _calendar_from(raw: dict) -> Calendar:
    return Calendar(
        project_week_one_starts=date.fromisoformat(raw["project_week_one_starts"]),
        todo_week_one_starts=date.fromisoformat(raw["todo_week_one_starts"]),
        tablero_week_one_monday=date.fromisoformat(raw["tablero_week_one_monday"]),
        sprints=tuple(
            Sprint(sprint["name"], date.fromisoformat(sprint["starts"]), date.fromisoformat(sprint["ends"]))
            for sprint in raw["sprints"]
        ),
        milestones=tuple(
            Milestone(date.fromisoformat(milestone["date"]), milestone["name"])
            for milestone in raw["milestones"]
        ),
    )
