import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

# The cátedra's sheets pad dropdown cells with zero-width spaces, so "​Verde" and "Verde" must compare equal.
INVISIBLE_CHARACTERS = ("​", "‌", "‍", "﻿")


class LayoutChanged(Exception):
    """A label the parser relies on is no longer where the sheet used to have it."""


@dataclass(frozen=True)
class CellPosition:
    row: int
    column: int


def open_workbook(path: Path):
    """The values as the sheet last computed them."""
    # Imported here so `doctor` can report a missing openpyxl instead of failing at import time.
    import openpyxl

    return openpyxl.load_workbook(path, data_only=True)


def open_workbook_as_typed(path: Path):
    """Formulas instead of their values, to tell what someone typed from what the template computes."""
    import openpyxl

    return openpyxl.load_workbook(path, data_only=False)


def require_sheet(book, name: str):
    if name not in book.sheetnames:
        raise LayoutChanged(f"No sheet named {name!r}. Sheets: {', '.join(book.sheetnames)}")
    return book[name]


def visible_text(value) -> str:
    if value is None:
        return ""
    text = str(value)
    for character in INVISIBLE_CHARACTERS:
        text = text.replace(character, "")
    return " ".join(text.split())


def comparable_text(value) -> str:
    without_accents = unicodedata.normalize("NFKD", visible_text(value)).encode("ascii", "ignore").decode()
    return without_accents.lower()


def as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return None


def as_number(value) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


class SheetGrid:
    """Reads a sheet by its labels instead of fixed coordinates, so moved rows do not silently shift the data."""

    def __init__(self, sheet):
        self.sheet = sheet

    @property
    def last_row(self) -> int:
        return self.sheet.max_row

    @property
    def last_column(self) -> int:
        return self.sheet.max_column

    def value(self, row: int, column: int):
        return self.sheet.cell(row=row, column=column).value

    def text(self, row: int, column: int) -> str:
        return visible_text(self.value(row, column))

    def locate(self, label: str, *, after_row: int = 0, column: int | None = None) -> CellPosition | None:
        wanted = comparable_text(label)
        return self._first_cell(lambda text: text == wanted, after_row=after_row, column=column)

    def require(self, label: str, *, after_row: int = 0, column: int | None = None) -> CellPosition:
        position = self.locate(label, after_row=after_row, column=column)
        if position is None:
            raise LayoutChanged(f"Label {label!r} not found in sheet {self.sheet.title!r} after row {after_row}")
        return position

    def require_starting_with(self, prefix: str) -> CellPosition:
        """For labels that embed a figure the team edits, like "BAC VIGENTE (212 HH)"."""
        wanted = comparable_text(prefix)
        position = self._first_cell(lambda text: text.startswith(wanted), after_row=0, column=None)
        if position is None:
            raise LayoutChanged(f"No label starting with {prefix!r} in sheet {self.sheet.title!r}")
        return position

    def _first_cell(self, matches, *, after_row: int, column: int | None) -> CellPosition | None:
        columns = [column] if column else range(1, self.last_column + 1)
        for row in range(after_row + 1, self.last_row + 1):
            for candidate_column in columns:
                if matches(comparable_text(self.value(row, candidate_column))):
                    return CellPosition(row, candidate_column)
        return None

    def headers(self, row: int) -> dict[str, int]:
        return {
            comparable_text(self.value(row, column)): column
            for column in range(1, self.last_column + 1)
            if comparable_text(self.value(row, column))
        }

    def value_right_of(self, position: CellPosition, *, stop_at_labels: tuple[str, ...] = ()):
        stop_texts = {comparable_text(label) for label in stop_at_labels}
        for column in range(position.column + 1, self.last_column + 1):
            current = self.value(position.row, column)
            if comparable_text(current) in stop_texts:
                return None
            if visible_text(current):
                return current
        return None


def cell_reference(sheet_title: str, cell: str) -> str:
    """Written the way the spreadsheet itself refers to a cell on another tab, so it can be pasted into the name box."""
    quoted_title = f"'{sheet_title}'" if " " in sheet_title else sheet_title
    return f"{quoted_title}!{cell}"


def column_letter(column: int) -> str:
    letters = ""
    while column > 0:
        column, remainder = divmod(column - 1, 26)
        letters = chr(ord("A") + remainder) + letters
    return letters


def column_starting_with(headers: dict[str, int], prefix: str, *, sheet_title: str) -> int:
    wanted = comparable_text(prefix)
    for header, column in headers.items():
        if header.startswith(wanted):
            return column
    raise LayoutChanged(f"No column starting with {prefix!r} in {sheet_title!r}. Headers: {', '.join(headers)}")
