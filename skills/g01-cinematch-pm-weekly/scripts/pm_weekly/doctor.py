import importlib.util
import shutil
from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .drive import drive_remotes
from .project import DRIVE_FOLDER_VARIABLE, KPI_PROJECT_VARIABLE, SETTINGS_GUIDE, MissingSetting, setting_from_environment
from .shell import CommandFailed, CommandRunner, run_command

SETUP_GUIDE = "references/setup.md"


@dataclass(frozen=True)
class Check:
    name: str
    ready: bool
    detail: str
    fix: str = ""


def run_checks(timezone: str, run: CommandRunner = run_command) -> list[Check]:
    return [
        _python_package("openpyxl", reads="the Drive spreadsheets"),
        _timezone_data(timezone),
        _rclone(run),
        _github_cli(run),
        _environment_setting(DRIVE_FOLDER_VARIABLE, needed_by="fetch"),
        _environment_setting(KPI_PROJECT_VARIABLE, needed_by="kpis"),
    ]


def _environment_setting(variable: str, *, needed_by: str) -> Check:
    """Never prints the value: only whether it is set."""
    try:
        setting_from_environment(variable)
        return Check(variable, True, "set")
    except MissingSetting:
        return Check(variable, False, f"not set, needed by `{needed_by}`", SETTINGS_GUIDE)


def _python_package(package: str, *, reads: str) -> Check:
    if importlib.util.find_spec(package):
        return Check(package, True, "installed")
    return Check(package, False, f"missing, needed to read {reads}", f"pip install {package}  ({SETUP_GUIDE}#python)")


def _timezone_data(timezone: str) -> Check:
    try:
        ZoneInfo(timezone)
        return Check("timezone data", True, timezone)
    except ZoneInfoNotFoundError:
        return Check("timezone data", False, f"{timezone} unknown to Python", f"pip install tzdata  ({SETUP_GUIDE}#python)")


def _rclone(run: CommandRunner) -> Check:
    if not shutil.which("rclone"):
        return Check("rclone", False, "not installed", f"{SETUP_GUIDE}#rclone")
    remotes = drive_remotes(run)
    if not remotes:
        return Check("rclone", False, "installed, but no Google Drive remote configured", f"{SETUP_GUIDE}#rclone")
    if len(remotes) > 1:
        return Check("rclone", True, f"Drive remotes {', '.join(remotes)}: pass --remote to fetch")
    return Check("rclone", True, f"Drive remote {remotes[0]!r}")


def _github_cli(run: CommandRunner) -> Check:
    if not shutil.which("gh"):
        return Check("gh", False, "not installed", f"{SETUP_GUIDE}#github")
    try:
        run(["gh", "auth", "status"])
        return Check("gh", True, "logged in")
    except CommandFailed:
        return Check("gh", False, "installed, not logged in", f"gh auth login  ({SETUP_GUIDE}#github)")
