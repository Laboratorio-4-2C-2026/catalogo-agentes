from dataclasses import dataclass

from ..spreadsheets.budget import BudgetBridge, EvmSettings
from ..spreadsheets.evm import EvmSheet


class MeasurementMissing(Exception):
    """EV or AC is not loaded for a period the cut covers, so no figure at that cut can be trusted."""


@dataclass(frozen=True)
class Projection:
    method: str
    assumption: str
    estimate_at_completion_usd: float
    actual_cost_usd: float
    budget_usd: float

    @property
    def estimate_to_complete_usd(self) -> float:
        return self.estimate_at_completion_usd - self.actual_cost_usd

    @property
    def variance_at_completion_usd(self) -> float:
        return self.budget_usd - self.estimate_at_completion_usd


@dataclass(frozen=True)
class PeriodPoint:
    period: int
    planned_hours: float
    earned_hours: float | None
    actual_hours: float | None
    planned_cumulative_hours: float
    earned_cumulative_hours: float | None
    actual_cumulative_hours: float | None


@dataclass(frozen=True)
class EarnedValueCut:
    """Every Steering figure in HH; USD is HH times the workbook's reference rate."""

    cut: int
    rate_per_hour: float
    budget_hours: float
    planned_hours: float
    earned_hours: float
    actual_hours: float
    capacity_per_period: float
    last_period: int

    def usd(self, hours: float) -> float:
        return hours * self.rate_per_hour

    @property
    def schedule_variance_hours(self) -> float:
        return self.earned_hours - self.planned_hours

    @property
    def cost_variance_hours(self) -> float:
        return self.earned_hours - self.actual_hours

    @property
    def schedule_performance_index(self) -> float:
        return self.earned_hours / self.planned_hours

    @property
    def cost_performance_index(self) -> float:
        return self.earned_hours / self.actual_hours

    @property
    def to_complete_performance_index(self) -> float:
        return (self.budget_hours - self.earned_hours) / (self.budget_hours - self.actual_hours)

    @property
    def physical_progress(self) -> float:
        return self.earned_hours / self.budget_hours

    @property
    def capacity_left_hours(self) -> float:
        return (self.last_period - self.cut) * self.capacity_per_period

    def projections(self) -> list[Projection]:
        budget = self.usd(self.budget_hours)
        actual = self.usd(self.actual_hours)
        remaining_work = self.usd(self.budget_hours - self.earned_hours)
        both_indices = self.cost_performance_index * self.schedule_performance_index
        estimates = [
            ("BAC / CPI", "typical: the current CPI holds until the end", budget / self.cost_performance_index),
            ("AC + (BAC - EV)", "the cost deviation was atypical and does not repeat", actual + remaining_work),
            ("AC + (BAC - EV) / (CPI x SPI)", "cost efficiency and pace both hold", actual + remaining_work / both_indices),
            ("AC + capacity left", "the developers work every hour until the end", actual + self.usd(self.capacity_left_hours)),
        ]
        return [
            Projection(
                method=method,
                assumption=assumption,
                estimate_at_completion_usd=estimate,
                actual_cost_usd=actual,
                budget_usd=budget,
            )
            for method, assumption, estimate in estimates
        ]


def earned_value_at(sheet: EvmSheet, settings: EvmSettings, *, cut: int) -> EarnedValueCut:
    missing = sheet.periods_missing_until(cut)
    if missing:
        periods = ", ".join(f"P{period}" for period in missing)
        raise MeasurementMissing(f"EV or AC is not loaded for {periods} in {sheet.title!r}; load them before measuring at P{cut}")
    return EarnedValueCut(
        cut=cut,
        rate_per_hour=settings.rate_per_hour.value,
        budget_hours=sheet.budget_at_completion,
        planned_hours=sheet.planned.cumulative_until(cut),
        earned_hours=sheet.earned.cumulative_until(cut),
        actual_hours=sheet.actual.cumulative_until(cut),
        capacity_per_period=settings.capacity_per_period.value,
        last_period=max(sheet.periods),
    )


def period_points(sheet: EvmSheet, *, cut: int) -> list[PeriodPoint]:
    points = []
    for period in sheet.periods:
        measured = period <= cut
        points.append(PeriodPoint(
            period=period,
            planned_hours=sheet.planned.values.get(period, 0.0),
            earned_hours=sheet.earned.values.get(period) if measured else None,
            actual_hours=sheet.actual.values.get(period) if measured else None,
            planned_cumulative_hours=sheet.planned.cumulative_until(period),
            earned_cumulative_hours=sheet.earned.cumulative_until(period) if measured else None,
            actual_cumulative_hours=sheet.actual.cumulative_until(period) if measured else None,
        ))
    return points


@dataclass(frozen=True)
class BudgetFigures:
    """The budget bridge rebuilt from the EVM tab's planned value, which is the baseline the EVM measures against."""

    budget_usd: float
    opex_usd: float
    contingency_rate: float
    charter_envelope_usd: float

    @property
    def cost_baseline_usd(self) -> float:
        return self.budget_usd + self.opex_usd

    @property
    def contingency_usd(self) -> float:
        return self.cost_baseline_usd * self.contingency_rate

    @property
    def total_authorized_usd(self) -> float:
        return self.cost_baseline_usd + self.contingency_usd

    @property
    def envelope_margin_usd(self) -> float:
        return self.charter_envelope_usd - self.total_authorized_usd


def budget_figures(earned_value: EarnedValueCut, settings: EvmSettings, bridge: BudgetBridge) -> BudgetFigures:
    return BudgetFigures(
        budget_usd=earned_value.usd(earned_value.budget_hours),
        opex_usd=settings.opex.value,
        contingency_rate=bridge.contingency.value / bridge.cost_baseline.value,
        charter_envelope_usd=bridge.charter_envelope.value,
    )
