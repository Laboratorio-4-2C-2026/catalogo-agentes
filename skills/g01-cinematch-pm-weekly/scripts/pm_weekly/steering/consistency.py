from dataclasses import dataclass

from ..spreadsheets.budget import BudgetBridge, EvmIndicators, EvmSettings, LabelledValue
from ..spreadsheets.workbook import cell_reference
from .earned_value import BudgetFigures, EarnedValueCut

# Below these, a difference is rounding: a dollar, the second decimal of an index, a tenth of a percentage point.
USD_TOLERANCE = 1.0
INDEX_TOLERANCE = 0.005
SHARE_TOLERANCE = 0.0005


@dataclass(frozen=True)
class Discrepancy:
    cell: str
    workbook_value: float
    recomputed_value: float
    unit: str
    consequence: str


@dataclass(frozen=True)
class WorkbookTabs:
    settings: EvmSettings
    bridge: BudgetBridge
    budget_tab: str
    indicators: EvmIndicators
    evm_tab: str


def discrepancies(earned_value: EarnedValueCut, figures: BudgetFigures, tabs: WorkbookTabs) -> list[Discrepancy]:
    """Each figure the workbook shows, against the same figure rebuilt from the EVM tab's period rows."""
    compared = [
        _compare(
            shown=tabs.settings.measurement_cut,
            tab=tabs.settings.sheet_title,
            recomputed=earned_value.cut,
            unit="period",
            tolerance=0.0,
            consequence="the workbook's USD rows, indicators and curves stop at its cut",
        ),
        _compare(
            shown=tabs.bridge.current_bac,
            tab=tabs.budget_tab,
            recomputed=figures.budget_usd,
            unit="USD",
            tolerance=USD_TOLERANCE,
            consequence="the budget tab holds a different baseline from the planned value the EVM measures against",
        ),
        _compare(
            shown=tabs.bridge.total_authorized,
            tab=tabs.budget_tab,
            recomputed=figures.total_authorized_usd,
            unit="USD",
            tolerance=USD_TOLERANCE,
            consequence="the total budget on the slide would not match the workbook",
        ),
        _compare(
            shown=tabs.indicators.schedule_performance_index,
            tab=tabs.evm_tab,
            recomputed=earned_value.schedule_performance_index,
            unit="index",
            tolerance=INDEX_TOLERANCE,
            consequence="the SPI on the slide would not match the workbook",
        ),
        _compare(
            shown=tabs.indicators.cost_performance_index,
            tab=tabs.evm_tab,
            recomputed=earned_value.cost_performance_index,
            unit="index",
            tolerance=INDEX_TOLERANCE,
            consequence="the CPI on the slide would not match the workbook",
        ),
        _compare(
            shown=tabs.indicators.physical_progress,
            tab=tabs.evm_tab,
            recomputed=earned_value.physical_progress,
            unit="share",
            tolerance=SHARE_TOLERANCE,
            consequence="the physical progress on the slide and in the Tablero would not match the workbook",
        ),
    ]
    return [discrepancy for discrepancy in compared if discrepancy is not None]


def _compare(
    *,
    shown: LabelledValue,
    tab: str,
    recomputed: float,
    unit: str,
    tolerance: float,
    consequence: str,
) -> Discrepancy | None:
    if abs(shown.value - recomputed) <= tolerance:
        return None
    return Discrepancy(cell_reference(tab, shown.cell), shown.value, recomputed, unit, consequence)
