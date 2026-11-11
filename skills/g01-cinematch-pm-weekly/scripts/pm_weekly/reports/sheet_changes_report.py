from datetime import date, datetime

from ..spreadsheets.sheet_diff import CellChange
from ..spreadsheets.workbook import cell_reference

LONGEST_TEXT_SHOWN = 80


def print_sheet_changes(changes_by_file: dict[str, list[CellChange]]) -> None:
    for file_name, changes in changes_by_file.items():
        print(f"{file_name}: {len(changes)} changed cells" if changes else f"{file_name}: no changes")
        for change in changes:
            print(f"  {cell_reference(change.sheet, change.cell)}: {_shown(change.before)} -> {_shown(change.after)}")


def _shown(value) -> str:
    if value is None or value == "":
        return "(empty)"
    if isinstance(value, (datetime, date)):
        return f"{value:%d/%m/%Y}"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:g}"
    text = str(value)
    return repr(text if len(text) <= LONGEST_TEXT_SHOWN else f"{text[:LONGEST_TEXT_SHOWN]}...")
