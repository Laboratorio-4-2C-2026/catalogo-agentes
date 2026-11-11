from dataclasses import dataclass

from .workbook import CellPosition, LayoutChanged, SheetGrid, as_number, column_letter, require_sheet

RATE_LABEL = "TARIFA DE REFERENCIA DEV"
CAPACITY_LABEL = "CAPACIDAD REAL"
CUT_LABEL = "FECHA DE CORTE"
BASELINE_PERIODS_LABEL = "PERIODOS DE LA LINEA BASE VIGENTE"
OPEX_LABEL = "TOTAL OPEX"
CURRENT_BAC_LABEL = "BAC VIGENTE"
ORIGINAL_BAC_LABEL = "BAC original"
COST_BASELINE_LABEL = "LINEA BASE DE COSTOS"
CONTINGENCY_LABEL = "Reserva de contingencia"
TOTAL_BUDGET_LABEL = "PRESUPUESTO TOTAL AUTORIZADO"
CHARTER_ENVELOPE_LABEL = "Presupuesto del Project Charter"
PHYSICAL_PROGRESS_LABEL = "% de avance fisico"


@dataclass(frozen=True)
class LabelledValue:
    cell: str
    value: float


@dataclass(frozen=True)
class EvmSettings:
    """The inputs the team workbook's EVM tab computes from, on its settings tab."""

    sheet_title: str
    rate_per_hour: LabelledValue
    capacity_per_period: LabelledValue
    measurement_cut: LabelledValue
    baseline_periods: LabelledValue
    opex: LabelledValue


@dataclass(frozen=True)
class BudgetBridge:
    """The reconciliation block at the bottom of the budget tab, in USD."""

    current_bac: LabelledValue
    original_bac: LabelledValue
    cost_baseline: LabelledValue
    contingency: LabelledValue
    total_authorized: LabelledValue
    charter_envelope: LabelledValue


def read_evm_settings(book, sheet_name: str) -> EvmSettings:
    grid = SheetGrid(require_sheet(book, sheet_name))
    return EvmSettings(
        sheet_title=sheet_name,
        rate_per_hour=_value_labelled(grid, RATE_LABEL),
        capacity_per_period=_value_labelled(grid, CAPACITY_LABEL),
        measurement_cut=_value_labelled(grid, CUT_LABEL),
        baseline_periods=_value_labelled(grid, BASELINE_PERIODS_LABEL),
        opex=_value_labelled(grid, OPEX_LABEL),
    )


def read_budget_bridge(book, sheet_name: str) -> BudgetBridge:
    grid = SheetGrid(require_sheet(book, sheet_name))
    return BudgetBridge(
        current_bac=_value_labelled(grid, CURRENT_BAC_LABEL),
        original_bac=_value_labelled(grid, ORIGINAL_BAC_LABEL),
        cost_baseline=_value_labelled(grid, COST_BASELINE_LABEL),
        contingency=_value_labelled(grid, CONTINGENCY_LABEL),
        total_authorized=_value_labelled(grid, TOTAL_BUDGET_LABEL),
        charter_envelope=_value_labelled(grid, CHARTER_ENVELOPE_LABEL),
    )


@dataclass(frozen=True)
class EvmIndicators:
    """What the EVM tab itself shows at its cut, to compare against a recomputation."""

    schedule_performance_index: LabelledValue
    cost_performance_index: LabelledValue
    physical_progress: LabelledValue


def read_evm_indicators(book, sheet_name: str) -> EvmIndicators:
    grid = SheetGrid(require_sheet(book, sheet_name))
    # Exact labels: "SPI = EV / PV" and "CPI = EV / AC" above them hold the per-period rows, not the figure at the cut.
    return EvmIndicators(
        schedule_performance_index=_number_right_of(grid, grid.require("SPI"), "SPI"),
        cost_performance_index=_number_right_of(grid, grid.require("CPI"), "CPI"),
        physical_progress=_value_labelled(grid, PHYSICAL_PROGRESS_LABEL),
    )


def _value_labelled(grid: SheetGrid, label_prefix: str) -> LabelledValue:
    return _number_right_of(grid, grid.require_starting_with(label_prefix), label_prefix)


def _number_right_of(grid: SheetGrid, label: CellPosition, label_text: str) -> LabelledValue:
    """The first number to the right of the label, so a value placed in column B or E is found the same way."""
    for column in range(label.column + 1, grid.last_column + 1):
        number = as_number(grid.value(label.row, column))
        if number is not None:
            return LabelledValue(f"{column_letter(column)}{label.row}", number)
    raise LayoutChanged(f"No number right of {label_text!r} in sheet {grid.sheet.title!r} row {label.row}")
