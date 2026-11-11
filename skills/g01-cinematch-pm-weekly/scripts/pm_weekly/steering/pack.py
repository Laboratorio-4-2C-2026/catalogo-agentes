from pathlib import Path

from ..project import Project
from ..reports.steering_report import print_steering_pack
from ..schedule import evm_period_containing, evm_period_dates
from ..spreadsheets.budget import read_budget_bridge, read_evm_indicators, read_evm_settings
from ..spreadsheets.evm import read_evm, read_original_plan_curve
from .consistency import WorkbookTabs, discrepancies
from .earned_value import BudgetFigures, EarnedValueCut, PeriodPoint, budget_figures, earned_value_at, period_points
from .s_curve_svg import CurveInput, Milestone, s_curve_svg


def present_steering_pack(evm_book, project: Project, *, cut: int | None, svg_path: Path | None) -> None:
    sheet = read_evm(evm_book, project.evm_sheet)
    settings = read_evm_settings(evm_book, project.evm_settings_sheet)
    earned_value = earned_value_at(sheet, settings, cut=cut or int(settings.measurement_cut.value))
    bridge = read_budget_bridge(evm_book, project.budget_sheet)
    figures = budget_figures(earned_value, settings, bridge)
    tabs = WorkbookTabs(
        settings=settings,
        bridge=bridge,
        budget_tab=project.budget_sheet,
        indicators=read_evm_indicators(evm_book, project.evm_sheet),
        evm_tab=project.evm_sheet,
    )
    points = period_points(sheet, cut=earned_value.cut)
    print_steering_pack(
        earned_value,
        figures,
        points,
        discrepancies(earned_value, figures, tabs),
        cut_dates=evm_period_dates(earned_value.cut, project.calendar),
    )
    if svg_path:
        original_plan = read_original_plan_curve(evm_book, project.evm_sheet)
        svg_path.write_text(s_curve_svg(_curve_input(project, earned_value, points, figures, original_plan)), encoding="utf-8")
        print(f"\nS-curve written to {svg_path}")


def _curve_input(
    project: Project,
    earned_value: EarnedValueCut,
    points: list[PeriodPoint],
    figures: BudgetFigures,
    original_plan: dict[int, float],
) -> CurveInput:
    periods = range(1, earned_value.last_period + 1)
    milestones = [
        Milestone(evm_period_containing(milestone.day, project.calendar), milestone.name)
        for milestone in project.calendar.milestones
    ]
    return CurveInput(
        earned_value=earned_value,
        points=points,
        original_plan_usd=original_plan,
        total_budget_usd=figures.total_authorized_usd,
        milestones=[milestone for milestone in milestones if milestone.period in periods],
        period_ends={period: evm_period_dates(period, project.calendar)[1] for period in periods},
    )
