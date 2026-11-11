from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from ..steering.consistency import Discrepancy
from ..steering.earned_value import BudgetFigures, EarnedValueCut, PeriodPoint

# Floats like 437.49999999 must print as the 437.5 they stand for before rounding half up, as a person would.
FLOAT_NOISE_DIGITS = 6


def print_steering_pack(
    earned_value: EarnedValueCut,
    figures: BudgetFigures,
    points: list[PeriodPoint],
    found_discrepancies: list[Discrepancy],
    *,
    cut_dates: tuple[date, date],
) -> None:
    start, end = cut_dates
    print(f"Steering pack · cut P{earned_value.cut} ({start:%d/%m} to {end:%d/%m}) · USD {earned_value.rate_per_hour:.2f} per HH")
    print("Every figure is rebuilt from the EVM tab's period rows; rounding is half up, once, at the end.")
    _print_budget(earned_value, figures)
    _print_indices(earned_value)
    _print_projections(earned_value)
    _print_periods(earned_value, points)
    _print_consistency(found_discrepancies)


def _print_budget(earned_value: EarnedValueCut, figures: BudgetFigures) -> None:
    print("\nBUDGET")
    rows = [
        ("BAC", f"{_hours(earned_value.budget_hours)} HH", figures.budget_usd, ""),
        ("OPEX", "", figures.opex_usd, ""),
        ("Cost baseline", "", figures.cost_baseline_usd, ""),
        (f"Contingency ({_percent(figures.contingency_rate, digits=0)})", "", figures.contingency_usd, ""),
        ("Total authorized", "", figures.total_authorized_usd, ""),
        ("Project Charter envelope", "", figures.charter_envelope_usd, f"margin {_usd(figures.envelope_margin_usd, signed=True)}"),
    ]
    for label, hours, amount, note in rows:
        print(f"  {label:<26}{hours:>10}  {_usd(amount):>8}  {note}".rstrip())


def _print_indices(earned_value: EarnedValueCut) -> None:
    usd = earned_value.usd
    print(f"\nEARNED VALUE AT P{earned_value.cut} (cumulative from P1)")
    for name, hours in (("PV", earned_value.planned_hours), ("EV", earned_value.earned_hours), ("AC", earned_value.actual_hours)):
        print(f"  {name}  {_hours(hours):>7} HH  {_usd(usd(hours)):>8}")
    print(
        f"  SV  {_hours(earned_value.schedule_variance_hours, signed=True):>7} HH  "
        f"{_usd(usd(earned_value.schedule_variance_hours), signed=True):>8}   SPI {_index(earned_value.schedule_performance_index)}"
    )
    print(
        f"  CV  {_hours(earned_value.cost_variance_hours, signed=True):>7} HH  "
        f"{_usd(usd(earned_value.cost_variance_hours), signed=True):>8}   CPI {_index(earned_value.cost_performance_index)}"
    )
    print(
        f"  TCPI {_index(earned_value.to_complete_performance_index)} · "
        f"physical progress {_percent(earned_value.physical_progress, digits=1)} of the BAC"
    )


def _print_projections(earned_value: EarnedValueCut) -> None:
    print("\nPROJECTIONS AT COMPLETION (USD)")
    for projection in earned_value.projections():
        print(
            f"  {projection.method:<30} ETC {_usd(projection.estimate_to_complete_usd):>7}  "
            f"EAC {_usd(projection.estimate_at_completion_usd):>7}  "
            f"VAC {_usd(projection.variance_at_completion_usd, signed=True):>7}  ({projection.assumption})"
        )


def _print_periods(earned_value: EarnedValueCut, points: list[PeriodPoint]) -> None:
    usd = earned_value.usd
    print("\nPERIODS (HH of each period; cumulative EV - PV in HH; cumulative USD for the S-curve)")
    print(f"  {'':4}{'PV':>6}{'EV':>6}{'AC':>6}{'EV-PV':>8}{'PV $':>9}{'EV $':>9}{'AC $':>9}")
    for point in points:
        gap = None if point.earned_cumulative_hours is None else point.earned_cumulative_hours - point.planned_cumulative_hours
        print(
            f"  P{point.period:<3}{_hours(point.planned_hours):>6}{_optional_hours(point.earned_hours):>6}"
            f"{_optional_hours(point.actual_hours):>6}{_optional_hours(gap, signed=True):>8}"
            f"{_usd(usd(point.planned_cumulative_hours)):>9}{_optional_usd(point.earned_cumulative_hours, usd):>9}"
            f"{_optional_usd(point.actual_cumulative_hours, usd):>9}"
        )


def _print_consistency(found_discrepancies: list[Discrepancy]) -> None:
    print("\nCONSISTENCY WITH WHAT THE WORKBOOK SHOWS")
    if not found_discrepancies:
        print("  OK: the workbook shows the same figures")
        return
    for discrepancy in found_discrepancies:
        print(
            f"  {discrepancy.cell}: the workbook shows {_unit_value(discrepancy.workbook_value, discrepancy.unit)}, "
            f"rebuilt it is {_unit_value(discrepancy.recomputed_value, discrepancy.unit)}: {discrepancy.consequence}"
        )


def _unit_value(value: float, unit: str) -> str:
    match unit:
        case "USD":
            return _usd(value)
        case "share":
            return _percent(value, digits=1)
        case "index":
            return _index(value)
        case _:
            return f"{value:g}"


def _rounded(value: float, digits: int) -> Decimal:
    exponent = Decimal(1).scaleb(-digits)
    return Decimal(str(round(value, FLOAT_NOISE_DIGITS))).quantize(exponent, rounding=ROUND_HALF_UP)


def _usd(amount: float, *, signed: bool = False) -> str:
    rounded = _rounded(amount, 0)
    sign = "+" if signed and rounded > 0 else "-" if rounded < 0 else ""
    return f"{sign}${abs(rounded):,}"


def _optional_usd(hours: float | None, usd) -> str:
    return "-" if hours is None else _usd(usd(hours))


def _hours(hours: float, *, signed: bool = False) -> str:
    return f"{_rounded(hours, 1):+}" if signed else f"{_rounded(hours, 1)}"


def _optional_hours(hours: float | None, *, signed: bool = False) -> str:
    return "-" if hours is None else _hours(hours, signed=signed)


def _index(value: float) -> str:
    return f"{_rounded(value, 2)}"


def _percent(share: float, *, digits: int) -> str:
    return f"{_rounded(share * 100, digits)}%"
