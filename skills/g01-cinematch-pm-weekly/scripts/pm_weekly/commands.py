import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from . import drive, github, kpi_watch, kpis
from .doctor import run_checks
from .project import MissingSetting, Project, load_project
from .reports.activity_reports import print_checks, print_kpi_compliance, print_pull_requests
from .reports.kpi_watch_report import WatchedWorkflow, print_kpi_watch
from .reports.plan_reports import print_calendar, print_evm, print_gantt_tasks, print_points
from .reports.review_queue_report import RepositoryContext, print_review_queue
from .reports.sheet_changes_report import print_sheet_changes
from .reports.tablero_report import print_tablero
from .review_queue.blockers import review_queue_of
from .review_queue.open_pull_requests import list_open_pull_requests
from .schedule import position_on
from .shell import CommandFailed
from .spreadsheets.budget import read_evm_settings
from .spreadsheets.evm import read_evm
from .spreadsheets.gantt import points_for, read_gantt
from .spreadsheets.sheet_diff import changed_cells
from .spreadsheets.tablero import read_tablero
from .spreadsheets.tablero_checks import current_week, find_gaps
from .spreadsheets.template_formulas import template_formula_findings
from .spreadsheets.workbook import LayoutChanged, open_workbook, open_workbook_as_typed
from .steering.earned_value import MeasurementMissing
from .steering.pack import present_steering_pack

KPI_RUNS_TO_READ = 40
KPI_WATCH_CLOSED_DAYS = 3
# Commits and checks cost about 10,000 GraphQL nodes per pull request, and GitHub refuses a query
# above 500,000: past about 48 the listing fails outright.
OPEN_PULL_REQUESTS_TO_READ = 30


def main(arguments: list[str]) -> int:
    project = load_project()
    options = _parser(project).parse_args(arguments)
    try:
        options.handler(options, project)
        return 0
    except (LayoutChanged, CommandFailed, FileNotFoundError, MeasurementMissing, MissingSetting) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


def _parser(project: Project) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pm.py", description="Cinematch PM weekly checks")
    commands = parser.add_subparsers(required=True, metavar="command")
    as_of = argparse.ArgumentParser(add_help=False)
    as_of.add_argument("--as-of", type=date.fromisoformat, default=_today(project), help="YYYY-MM-DD, default today")
    source = argparse.ArgumentParser(add_help=False)
    source.add_argument("source", type=Path, help="the exported .xlsx, or the folder `fetch` exported into")
    _add_setup_commands(commands, as_of=as_of)
    _add_spreadsheet_commands(commands, as_of=as_of, source=source)
    _add_activity_commands(commands, as_of=as_of)
    return parser


def _add_setup_commands(commands, *, as_of) -> None:
    commands.add_parser("doctor", help="check rclone, gh and Python packages").set_defaults(handler=_doctor)
    commands.add_parser("calendar", parents=[as_of], help="this week in every numbering").set_defaults(handler=_calendar)
    fetch = commands.add_parser("fetch", help="export the Drive spreadsheets with rclone")
    fetch.add_argument("destination", type=Path, help="a scratch folder outside the vault")
    fetch.add_argument("--remote", help="rclone remote, when there is more than one Drive remote")
    fetch.set_defaults(handler=_fetch)


def _add_spreadsheet_commands(commands, *, as_of, source) -> None:
    commands.add_parser("tablero", parents=[as_of, source], help="gaps in the Tablero").set_defaults(handler=_tablero)
    evm = commands.add_parser("evm", parents=[as_of, source], help="earned value loaded so far")
    evm.add_argument("--catedra", action="store_true", help="read the cátedra's 10B workbook instead of the team's")
    evm.set_defaults(handler=_evm)
    gantt = commands.add_parser("gantt", parents=[source], help="baseline tasks and their points")
    gantt.add_argument("--week", type=int, help="only tasks planned for this gantt week")
    gantt.add_argument("--ids", help="comma-separated task ids whose baseline points to add up")
    gantt.set_defaults(handler=_gantt)
    diff = commands.add_parser("diff", help="cells someone changed between two exports, formulas included")
    diff.add_argument("before", type=Path, help="the folder of an earlier `fetch`")
    diff.add_argument("after", type=Path, help="the folder of a later `fetch`")
    diff.set_defaults(handler=_diff)
    steering = commands.add_parser("steering", parents=[source], help="budget, EVM and S-curve figures for a Steering")
    steering.add_argument("--cut", type=int, help="the period to measure at, default the workbook's own cut")
    steering.add_argument("--svg", type=Path, help="also write the S-curve as SVG to this file")
    steering.set_defaults(handler=_steering)


def _add_activity_commands(commands, *, as_of) -> None:
    commands.add_parser("kpis", parents=[as_of], help="daily KPI compliance from the platform").set_defaults(handler=_kpis)
    commands.add_parser(
        "kpi-watch", parents=[as_of], help="whether today's KPIs went out, and what to do before midnight if not"
    ).set_defaults(handler=_kpi_watch)
    prs = commands.add_parser("prs", help="app pull requests grouped by Linear issue")
    prs.add_argument("--since", type=date.fromisoformat, help="only PRs opened or merged since YYYY-MM-DD")
    prs.add_argument("--limit", type=int, default=100)
    prs.set_defaults(handler=_prs)
    blockers = commands.add_parser("blockers", help="open pull requests stuck in review or waiting to merge, and who has to act")
    blockers.add_argument("--limit", type=int, default=OPEN_PULL_REQUESTS_TO_READ)
    blockers.set_defaults(handler=_blockers)


def _doctor(options, project: Project) -> None:
    print_checks(run_checks(project.timezone))


def _calendar(options, project: Project) -> None:
    print_calendar(position_on(options.as_of, project.calendar), project.calendar)


def _fetch(options, project: Project) -> None:
    remote = options.remote or _only_drive_remote()
    options.destination.mkdir(parents=True, exist_ok=True)
    output = drive.export_from_folder(
        remote=remote,
        folder_id=project.drive_folder_id,
        file_names=list(project.drive_files.values()),
        destination=options.destination,
    )
    for notice in output.stderr.splitlines():
        print(notice)
    for file_name in project.drive_files.values():
        exported = options.destination / file_name
        print(f"{'OK     ' if exported.exists() else 'MISSING'} {exported}")


def _only_drive_remote() -> str:
    remotes = drive.drive_remotes()
    if len(remotes) != 1:
        found = ", ".join(remotes) or "none"
        raise CommandFailed(["rclone", "listremotes"], f"expected one Google Drive remote, found {found}: pass --remote")
    return remotes[0]


def _tablero(options, project: Project) -> None:
    path = _resolve(options.source, project.drive_file("tablero"))
    tablero = read_tablero(open_workbook(path), project.tablero_tab, year=options.as_of.year)
    findings = [
        *find_gaps(tablero, options.as_of),
        *template_formula_findings(open_workbook_as_typed(path), tablero),
    ]
    print_tablero(tablero, current_week(tablero, options.as_of), findings)


def _evm(options, project: Project) -> None:
    last_closed_period = position_on(options.as_of, project.calendar).last_closed_evm_period
    if options.catedra:
        book = open_workbook(_resolve(options.source, project.drive_file("evm_catedra")))
        print_evm(read_evm(book, project.evm_catedra_sheet), last_closed_period, settings=None)
        return
    book = open_workbook(_resolve(options.source, project.drive_file("evm")))
    settings = read_evm_settings(book, project.evm_settings_sheet)
    print_evm(read_evm(book, project.evm_sheet), last_closed_period, settings=settings)


def _diff(options, project: Project) -> None:
    changes_by_file = {}
    for file_key, file_name in project.drive_files.items():
        before = open_workbook_as_typed(_resolve(options.before, file_name))
        after = open_workbook_as_typed(_resolve(options.after, file_name))
        # The Tablero holds every team's tab; only ours is compared, so no other team's data is printed.
        sheet_names = [project.tablero_tab] if file_key == "tablero" else after.sheetnames
        changes_by_file[file_name] = changed_cells(before, after, sheet_names=sheet_names)
    print_sheet_changes(changes_by_file)


def _steering(options, project: Project) -> None:
    book = open_workbook(_resolve(options.source, project.drive_file("evm")))
    present_steering_pack(book, project, cut=options.cut, svg_path=options.svg)


def _gantt(options, project: Project) -> None:
    tasks = read_gantt(open_workbook(_resolve(options.source, project.drive_file("gantt"))), project.gantt_sheet)
    if options.ids:
        print_points(*points_for(tasks, options.ids.split(",")))
        return
    print_gantt_tasks(tuple(task for task in tasks if options.week in (None, task.week)))


def _kpis(options, project: Project) -> None:
    window, days = _load_compliance(project, until=options.as_of)
    print_kpi_compliance(window, days, today=_today(project))


def _kpi_watch(options, project: Project) -> None:
    zone = ZoneInfo(project.timezone)
    now = datetime.now(zone)
    _, days = _load_compliance(project, until=options.as_of)
    compliance_by_day = {day.day: day for day in days}
    runs = github.list_workflow_runs(project.app_repository, project.kpi_workflow, limit=KPI_RUNS_TO_READ)
    schedule = kpi_watch.report_schedule(
        github.workflow_definition(project.app_repository, project.kpi_workflow), runs, today=now.date()
    )
    open_day = None
    if options.as_of == now.date():
        runs_today = kpi_watch.runs_on(now.date(), runs, zone)
        open_day = kpi_watch.watch_open_day(
            compliance_by_day.get(now.date()),
            runs_today,
            _deliveries(project, runs_today, compliance_by_day.get(now.date())),
            now=now,
            schedule=schedule,
        )
    closed_days = []
    for day in sorted((day for day in compliance_by_day if day < now.date()), reverse=True)[:KPI_WATCH_CLOSED_DAYS]:
        runs_of_the_day = kpi_watch.runs_on(day, runs, zone)
        deliveries = _deliveries(project, runs_of_the_day, compliance_by_day[day])
        closed_days.append(kpi_watch.watch_closed_day(compliance_by_day[day], runs_of_the_day, deliveries, day=day))
    workflow = WatchedWorkflow(project.kpi_workflow, project.app_repository, project.kpi_compliance_url)
    print_kpi_watch(open_day, closed_days, now=now, schedule=schedule, workflow=workflow)


def _deliveries(
    project: Project,
    runs_of_the_day: tuple[github.WorkflowRun, ...],
    compliance: kpis.DayCompliance | None,
) -> list[kpi_watch.DeliveredReport]:
    """Artifacts are only read when the data branch does not already show the day complete, since each one is a download."""
    if compliance and compliance.is_complete:
        return []
    return [
        kpi_watch.delivered_report(run.run_id, artifact_text)
        for run in runs_of_the_day
        if run.is_finished
        for artifact_text in github.run_artifact_texts(project.app_repository, run.run_id)
    ]


def _load_compliance(project: Project, *, until: date) -> tuple[kpis.GradingWindow, list[kpis.DayCompliance]]:
    return kpis.fetch_compliance(project.kpi_repository, project.kpi_branch, project_id=project.kpi_project_id, until=until)


def _prs(options, project: Project) -> None:
    zone = ZoneInfo(project.timezone)
    pull_requests = github.list_pull_requests(project.app_repository, limit=options.limit)
    if options.since:
        pull_requests = [pull_request for pull_request in pull_requests if _touched_since(pull_request, options.since, zone)]
    print_pull_requests(
        pull_requests,
        issue_key_pattern=github.issue_key_pattern(project.linear_team_key),
        team_key=project.linear_team_key,
        zone=zone,
    )


def _blockers(options, project: Project) -> None:
    now = datetime.now(ZoneInfo(project.timezone))
    open_pull_requests = list_open_pull_requests(project.app_repository, limit=options.limit)
    context = RepositoryContext(
        repository=project.app_repository,
        default_branch=project.app_default_branch,
        issue_key_pattern=github.issue_key_pattern(project.linear_team_key),
        team_key=project.linear_team_key,
    )
    queue = review_queue_of(open_pull_requests, default_branch=project.app_default_branch)
    print_review_queue(queue, now=now, context=context)


def _touched_since(pull_request: github.PullRequest, since: date, zone: ZoneInfo) -> bool:
    moments = [moment for moment in (pull_request.created_at, pull_request.merged_at) if moment]
    return any(moment.astimezone(zone).date() >= since for moment in moments)


def _resolve(source: Path, file_name: str) -> Path:
    path = source / file_name if source.is_dir() else source
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist; run `fetch` first")
    return path


def _today(project: Project) -> date:
    try:
        return datetime.now(ZoneInfo(project.timezone)).date()
    except ZoneInfoNotFoundError:
        # Falls back so `doctor` still runs and reports the missing timezone data.
        return date.today()
