import re
from collections import Counter
from dataclasses import dataclass

from .tablero import Tablero
from .tablero_checks import Finding, FindingKind
from .workbook import column_letter, require_sheet, visible_text

ROW_PLACEHOLDER = "{row}"
# Below this many rows sharing a formula, a column is not treated as carrying a template.
MINIMUM_TEMPLATE_ROWS = 3


@dataclass(frozen=True)
class OverriddenFormula:
    cell: str
    header: str
    template: str
    found: object


def template_formula_findings(typed_book, tablero: Tablero) -> list[Finding]:
    """Cells of the cátedra's template formulas that someone replaced by a typed value or a different formula."""
    sheet = require_sheet(typed_book, tablero.tab)
    blocks = (
        (tablero.activity_rows, [activity.row for activity in tablero.activities]),
        (tablero.incident_rows, [incident.row for incident in tablero.incidents]),
    )
    return [
        Finding(
            FindingKind.INCONSISTENT,
            overridden.cell,
            f"{overridden.header} holds {overridden.found!r} instead of the template's formula {overridden.template}",
        )
        for block_rows, filled_rows in blocks
        for overridden in overridden_formulas(sheet, block_rows=block_rows, filled_rows=filled_rows)
    ]


def overridden_formulas(sheet, *, block_rows: range, filled_rows: list[int]) -> list[OverriddenFormula]:
    header_row = block_rows.start - 1
    overridden = []
    for column in range(1, sheet.max_column + 1):
        template = _column_template(sheet, column, block_rows)
        if template is None:
            continue
        for row in filled_rows:
            found = sheet.cell(row=row, column=column).value
            if _shape(found, row) != template:
                overridden.append(OverriddenFormula(
                    cell=f"{column_letter(column)}{row}",
                    header=visible_text(sheet.cell(row=header_row, column=column).value),
                    template=template.replace(ROW_PLACEHOLDER, str(row)),
                    found=found,
                ))
    return overridden


def _column_template(sheet, column: int, rows: range) -> str | None:
    shapes = Counter(
        shape
        for row in rows
        if (shape := _shape(sheet.cell(row=row, column=column).value, row)) is not None
    )
    if not shapes:
        return None
    shape, rows_sharing_it = shapes.most_common(1)[0]
    return shape if rows_sharing_it >= MINIMUM_TEMPLATE_ROWS else None


def _shape(value, row: int) -> str | None:
    """A formula with its own row number abstracted, so the same template written on two rows compares equal."""
    if not (isinstance(value, str) and value.startswith("=")):
        return None
    return re.sub(rf"(?<=[A-Z]){row}(?!\d)", ROW_PLACEHOLDER, value)
