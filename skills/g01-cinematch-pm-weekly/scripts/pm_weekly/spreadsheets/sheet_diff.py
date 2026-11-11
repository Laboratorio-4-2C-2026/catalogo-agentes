from dataclasses import dataclass

from .workbook import column_letter

WHOLE_TAB = "(whole tab)"


@dataclass(frozen=True)
class CellChange:
    sheet: str
    cell: str
    before: object
    after: object


def changed_cells(before_book, after_book, *, sheet_names: list[str]) -> list[CellChange]:
    """Both books opened as typed, so a formula replaced by its own value shows up as a change."""
    return [change for name in sheet_names for change in _tab_changes(before_book, after_book, name)]


def _tab_changes(before_book, after_book, name: str) -> list[CellChange]:
    if name not in before_book.sheetnames or name not in after_book.sheetnames:
        return [CellChange(name, WHOLE_TAB, _presence(before_book, name), _presence(after_book, name))]
    before, after = before_book[name], after_book[name]
    changes = []
    for row in range(1, max(before.max_row, after.max_row) + 1):
        for column in range(1, max(before.max_column, after.max_column) + 1):
            old = _typed_content(before.cell(row=row, column=column).value)
            new = _typed_content(after.cell(row=row, column=column).value)
            if old != new:
                changes.append(CellChange(name, f"{column_letter(column)}{row}", old, new))
    return changes


def _typed_content(value):
    """openpyxl returns array formulas as objects that compare by identity, so they are compared by their formula text."""
    return getattr(value, "text", value)


def _presence(book, name: str) -> str:
    return "present" if name in book.sheetnames else "absent"
