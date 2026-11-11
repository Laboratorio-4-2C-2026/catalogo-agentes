"""The Steering S-curve as an SVG, in the look of the Steering 2 chart: dark slide, mono labels, nothing under 18 px."""
import math
from dataclasses import dataclass
from datetime import date

from .earned_value import EarnedValueCut, PeriodPoint

WIDTH, HEIGHT = 1920, 1080
PLOT_LEFT, PLOT_RIGHT, PLOT_TOP, PLOT_BOTTOM = 175, 1640, 160, 880
BACKGROUND, GRID, AXIS, TEXT = "#0B0B0B", "#3C3C3C", "#7A7A7A", "#DADADA"
PLANNED, EARNED, ACTUAL, ORIGINAL, HIGHLIGHT = "#FFD54A", "#4FD2FF", "#FF5A4A", "#C9A0FF", "#F2F2F2"
NICE_STEPS = (500, 1000, 2000, 2500, 5000)
GRID_LINES_WANTED = 5
STYLE = (
    "<style>"
    ".mono{font-family:'DejaVu Sans Mono',monospace}"
    ".sans{font-family:'Inter','Inter Display',sans-serif}"
    "</style>"
)


@dataclass(frozen=True)
class Milestone:
    period: int
    label: str


@dataclass(frozen=True)
class CurveInput:
    earned_value: EarnedValueCut
    points: list[PeriodPoint]
    original_plan_usd: dict[int, float]
    total_budget_usd: float
    milestones: list[Milestone]
    period_ends: dict[int, date]


def s_curve_svg(curve: CurveInput) -> str:
    canvas = _Canvas(periods=curve.earned_value.last_period, top_usd=_axis_top(curve))
    elements = [
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>',
        *_titles(curve),
        *_grid(canvas),
        *_period_axis(canvas, curve.period_ends),
        *_budget_lines(canvas, curve),
        *_milestone_lines(canvas, curve),
        *_series(canvas, curve),
        *_legend(curve),
    ]
    body = "\n".join(elements)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">\n{STYLE}\n{body}\n</svg>\n'


class _Canvas:
    """Maps a period and an amount in USD to pixels; period 0 is the origin of every curve."""

    def __init__(self, *, periods: int, top_usd: float):
        self.periods = periods
        self.top_usd = top_usd

    def x(self, period: float) -> float:
        return PLOT_LEFT + (PLOT_RIGHT - PLOT_LEFT) * period / self.periods

    def y(self, usd: float) -> float:
        return PLOT_BOTTOM - (PLOT_BOTTOM - PLOT_TOP) * usd / self.top_usd


def _axis_top(curve: CurveInput) -> float:
    earned_value = curve.earned_value
    highest = max(
        curve.total_budget_usd,
        earned_value.usd(earned_value.actual_hours + earned_value.capacity_left_hours),
        *curve.original_plan_usd.values(),
    )
    step = _grid_step(highest)
    return step * math.ceil(highest / step)


def _grid_step(highest_usd: float) -> int:
    return next((step for step in NICE_STEPS if highest_usd / step <= GRID_LINES_WANTED), NICE_STEPS[-1])


def _titles(curve: CurveInput) -> list[str]:
    cut = curve.earned_value.cut
    return [
        f'<text x="40" y="50" class="mono" font-size="28" font-weight="bold" fill="{PLANNED}" letter-spacing="2">CURVA S · PV / EV / AC</text>',
        f'<text x="40" y="84" class="sans" font-size="21" fill="{TEXT}">USD acumulados · proyecto completo (P1 a P{curve.earned_value.last_period}) · corte P{cut}</text>',
    ]


def _grid(canvas: _Canvas) -> list[str]:
    step = _grid_step(canvas.top_usd)
    elements = []
    for amount in range(0, int(canvas.top_usd) + 1, step):
        y = canvas.y(amount)
        elements.append(f'<line x1="{PLOT_LEFT}" y1="{y:.1f}" x2="{PLOT_RIGHT}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        elements.append(f'<text x="{PLOT_LEFT - 14}" y="{y + 7:.1f}" class="mono" font-size="19" fill="{TEXT}" text-anchor="end">{amount:,}</text>')
    return elements


def _period_axis(canvas: _Canvas, period_ends: dict[int, date]) -> list[str]:
    elements = [f'<line x1="{PLOT_LEFT}" y1="{PLOT_BOTTOM}" x2="{PLOT_RIGHT}" y2="{PLOT_BOTTOM}" stroke="{AXIS}" stroke-width="1.5"/>']
    for period in range(1, canvas.periods + 1):
        x = canvas.x(period)
        elements.append(f'<text x="{x:.1f}" y="{PLOT_BOTTOM + 32}" class="mono" font-size="21" font-weight="bold" fill="{PLANNED}" text-anchor="middle">P{period}</text>')
        if period in period_ends:
            elements.append(f'<text x="{x:.1f}" y="{PLOT_BOTTOM + 58}" class="mono" font-size="18" fill="{TEXT}" text-anchor="middle">{period_ends[period]:%d-%m}</text>')
    return elements


def _budget_lines(canvas: _Canvas, curve: CurveInput) -> list[str]:
    lines = [
        (curve.total_budget_usd, HIGHLIGHT, f"Presupuesto total ${curve.total_budget_usd:,.0f}"),
        (curve.earned_value.usd(curve.earned_value.budget_hours), PLANNED, f"BAC ${curve.earned_value.usd(curve.earned_value.budget_hours):,.0f}"),
    ]
    elements = []
    for amount, color, label in lines:
        y = canvas.y(amount)
        elements.append(f'<line x1="{PLOT_LEFT}" y1="{y:.1f}" x2="{PLOT_RIGHT}" y2="{y:.1f}" stroke="{color}" stroke-width="1.5" stroke-dasharray="3 6"/>')
        elements.append(f'<text x="{PLOT_RIGHT - 12}" y="{y - 10:.1f}" class="mono" font-size="18" font-weight="bold" fill="{color}" text-anchor="end">{label}</text>')
    return elements


def _milestone_lines(canvas: _Canvas, curve: CurveInput) -> list[str]:
    """Labels alternate between two rows so that milestones two periods apart do not overlap."""
    cut = curve.earned_value.cut
    markers = {milestone.period: milestone.label.upper() for milestone in curve.milestones}
    markers[cut] = f"{markers[cut]} · CORTE" if cut in markers else f"CORTE P{cut}"
    elements = []
    for index, period in enumerate(sorted(markers)):
        x, color = canvas.x(period), ACTUAL if period == cut else HIGHLIGHT
        label_y = PLOT_TOP - 22 if index % 2 == 0 else PLOT_TOP - 46
        elements.append(f'<line x1="{x:.1f}" y1="{PLOT_TOP}" x2="{x:.1f}" y2="{PLOT_BOTTOM}" stroke="{color}" stroke-width="2" stroke-dasharray="7 6"/>')
        elements.append(f'<text x="{x:.1f}" y="{label_y}" class="mono" font-size="18" font-weight="bold" fill="{color}" text-anchor="middle">{markers[period]}</text>')
    return elements


def _series(canvas: _Canvas, curve: CurveInput) -> list[str]:
    usd = curve.earned_value.usd
    planned = [(point.period, usd(point.planned_cumulative_hours)) for point in curve.points]
    earned = [(point.period, usd(point.earned_cumulative_hours)) for point in curve.points if point.earned_cumulative_hours is not None]
    actual = [(point.period, usd(point.actual_cumulative_hours)) for point in curve.points if point.actual_cumulative_hours is not None]
    elements = []
    if curve.original_plan_usd:
        elements.append(_path(canvas, sorted(curve.original_plan_usd.items()), ORIGINAL, width=3, dashes="2 8"))
    elements.append(_path(canvas, planned, PLANNED, width=4))
    elements.append(_path(canvas, _projected_actual(curve, actual), ACTUAL, width=3, dashes="10 8", from_origin=False))
    for points, color in ((actual, ACTUAL), (earned, EARNED)):
        elements.append(_path(canvas, points, color, width=4))
        elements.extend(_dots(canvas, points, color))
    return elements


def _projected_actual(curve: CurveInput, actual: list[tuple[int, float]]) -> list[tuple[int, float]]:
    """From the cut on, the actual cost keeps its slope: the team's capacity, every period until the end."""
    if not actual:
        return []
    cut_period, cut_amount = actual[-1]
    per_period = curve.earned_value.usd(curve.earned_value.capacity_per_period)
    return [(period, cut_amount + per_period * (period - cut_period)) for period in range(cut_period, curve.earned_value.last_period + 1)]


def _path(canvas: _Canvas, points: list[tuple[int, float]], color: str, *, width: int, dashes: str = "", from_origin: bool = True) -> str:
    coordinates = ([(0, 0.0)] if from_origin else []) + points
    commands = " ".join(f"{'M' if index == 0 else 'L'}{canvas.x(period):.1f} {canvas.y(amount):.1f}" for index, (period, amount) in enumerate(coordinates))
    dash_attribute = f' stroke-dasharray="{dashes}"' if dashes else ""
    return f'<path d="{commands}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attribute} stroke-linecap="round"/>'


def _dots(canvas: _Canvas, points: list[tuple[int, float]], color: str) -> list[str]:
    return [
        f'<circle cx="{canvas.x(period):.1f}" cy="{canvas.y(amount):.1f}" r="6.5" fill="{color}" stroke="{BACKGROUND}" stroke-width="2"/>'
        for period, amount in points
    ]


def _legend(curve: CurveInput) -> list[str]:
    """Top left of the plot, which an S-curve never reaches."""
    entries = [
        (PLANNED, "", "PV · línea base vigente"),
        (EARNED, "", "EV · valor ganado"),
        (ACTUAL, "", "AC · costo real"),
        (ACTUAL, "10 8", "AC proyectado a capacidad"),
    ]
    if curve.original_plan_usd:
        entries.append((ORIGINAL, "2 8", "PV · línea base original"))
    elements = []
    for index, (color, dashes, label) in enumerate(entries):
        y = PLOT_TOP + 40 + 34 * index
        dash_attribute = f' stroke-dasharray="{dashes}"' if dashes else ""
        elements.append(f'<line x1="{PLOT_LEFT + 30}" y1="{y}" x2="{PLOT_LEFT + 80}" y2="{y}" stroke="{color}" stroke-width="4"{dash_attribute}/>')
        elements.append(f'<text x="{PLOT_LEFT + 94}" y="{y + 7}" class="mono" font-size="19" fill="{TEXT}">{label}</text>')
    return elements
