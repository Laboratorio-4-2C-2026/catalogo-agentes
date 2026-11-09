"""Check the current report week and required cells from a read-only snapshot."""
import argparse
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def report_zone(context, at=None):
    try:
        return ZoneInfo(context["timezone"])
    except ZoneInfoNotFoundError:
        fallback = context.get("timezone_fallback", {})
        reference = at or datetime.now(timezone.utc)
        match = re.fullmatch(r"([+-])(\d{2}):(\d{2})", fallback.get("offset", ""))
        if not match:
            raise ValueError("Timezone data unavailable; use Python tzdata or an explicit valid fixed-offset fallback")
        sign, hours, minutes = match.groups()
        if int(hours) > 23 or int(minutes) > 59:
            raise ValueError("Invalid fixed timezone offset")
        delta = timedelta(hours=int(hours), minutes=int(minutes))
        zone = timezone(delta if sign == "+" else -delta)
        local_day = reference.astimezone(zone).date()
        if not (date.fromisoformat(fallback["valid_from"]) <= local_day <= date.fromisoformat(fallback["valid_until"])):
            raise ValueError("Configured fixed-offset fallback has expired")
        return zone


def col_number(label):
    result = 0
    for char in label.upper():
        if not "A" <= char <= "Z":
            raise ValueError("Invalid column: " + label)
        result = result * 26 + ord(char) - ord("A") + 1
    return result


def col_label(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def cell_value(values, row, column):
    if row < 1 or column < 1:
        raise ValueError("Rows and columns are one-based")
    if row > len(values) or column > len(values[row - 1]):
        return ""
    raw = values[row - 1][column - 1]
    return "" if raw is None else str(raw).strip()


def header_date(value, report_year):
    first_line = value.splitlines()[0].strip() if value else ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", first_line):
        return date.fromisoformat(first_line)
    match = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{2}|\d{4}))?", first_line)
    if not match:
        return None
    day, month, year = match.groups()
    if year is None and report_year is None:
        raise ValueError("A year is required for date headers without a year")
    year = report_year if year is None else int(year)
    if year < 100:
        year += 2000
    return date(year, int(month), int(day))


def check(context, snapshot, at, week_start=None):
    zone = report_zone(context, at)
    if at.tzinfo is None:
        raise ValueError("The cutoff needs an explicit timezone")
    at = at.astimezone(zone)
    source = snapshot.get("source", {})
    expected = context["sheet"]
    for key in ("spreadsheet_id", "gid", "sheet_name"):
        if str(source.get(key, "")) != str(expected[key]):
            return {"status": "UNVERIFIED", "reason": "Snapshot source mismatch: " + key}
    read_at = datetime.fromisoformat(source["read_at"].replace("Z", "+00:00"))
    if read_at.tzinfo is None:
        return {"status": "UNVERIFIED", "reason": "Snapshot timestamp needs a timezone"}
    age = (at - read_at.astimezone(zone)).total_seconds()
    max_age = context.get("max_snapshot_age_hours", 24) * 3600
    if age < -300 or age > max_age:
        return {"status": "UNVERIFIED", "reason": "Snapshot is stale or from the future"}
    values = snapshot["values"]
    weekly = context["weekly"]
    header_row = weekly["header_row"]
    needed_row = max([header_row] + [item["row"] for item in weekly["required_inputs"]] +
                     ([weekly["computed_summary"]["row"]] if weekly.get("computed_summary") else []))
    if len(values) < needed_row or len(values[header_row - 1]) < col_number(weekly["last_column"]):
        return {"status": "UNVERIFIED", "reason": "Snapshot does not cover the configured weekly grid"}
    label_column = col_number(weekly.get("labels_column", "A"))
    for item in weekly["required_inputs"]:
        label = cell_value(values, item["row"], label_column)
        if label.casefold() != item["name"].casefold():
            return {"status": "UNVERIFIED", "reason": "Row label changed: " + item["name"]}
    anchor = weekly.get("week_start_iso", 1)
    if anchor not in range(1, 8):
        raise ValueError("week_start_iso must be 1 through 7")
    current_week = at.date() - timedelta(days=(at.isoweekday() - anchor) % 7)
    week = date.fromisoformat(week_start) if week_start is not None else current_week
    if week.isoweekday() != anchor:
        raise ValueError("The requested week must start on the configured anchor weekday")
    found = []
    for column in range(col_number(weekly["first_column"]), col_number(weekly["last_column"]) + 1):
        value = cell_value(values, header_row, column)
        if header_date(value, context.get("report_year")) == week:
            found.append(column)
    if len(found) != 1:
        return {"status": "PERIOD_NOT_FOUND", "week_start": week.isoformat(),
                "reason": "Expected one matching date header; found " + str(len(found))}
    column = found[0]
    prefix = col_label(column)
    allowed = {v.casefold(): v for v in weekly["allowed_values"]}
    missing, invalid, observed, colors = [], [], {}, []
    for item in weekly["required_inputs"]:
        row = item["row"]
        reference = prefix + str(row)
        if len(values[row - 1]) < column:
            return {"status": "UNVERIFIED", "reason": "Snapshot does not cover " + reference}
        value = cell_value(values, row, column)
        observed[reference] = value
        if not value:
            missing.append({"cell": reference, "field": item["name"]})
            continue
        normalized = allowed.get(value.casefold())
        if normalized is None:
            invalid.append({"cell": reference, "value": value})
            continue
        colors.append(normalized)
        reasons = weekly.get("reasons", {})
        if normalized in reasons.get("required_for", []):
            reason_cell = reasons["column"] + str(row)
            if len(values[row - 1]) < col_number(reasons["column"]):
                return {"status": "UNVERIFIED", "reason": "Snapshot does not cover " + reason_cell}
            reason = cell_value(values, row, col_number(reasons["column"]))
            observed[reason_cell] = reason
            if not reason:
                missing.append({"cell": reason_cell, "field": "Motivo: " + item["name"]})
    summary = weekly.get("computed_summary")
    summary_check = None
    if summary and not missing and not invalid:
        rule = summary["rule"]
        if rule != "one_red_or_three_yellows":
            raise ValueError("Unsupported summary rule: " + rule)
        proposed = ("Rojo" if colors.count("Rojo") >= 1 or colors.count("Amarillo") >= 3
                    else "Amarillo" if "Amarillo" in colors else "Verde")
        reference = prefix + str(summary["row"])
        if len(values[summary["row"] - 1]) < column:
            return {"status": "UNVERIFIED", "reason": "Snapshot does not cover " + reference}
        actual = cell_value(values, summary["row"], column)
        summary_check = {"cell": reference, "observed": actual, "expected": proposed}
        if actual.casefold() != proposed.casefold():
            invalid.append(summary_check)
    return {"status": "INCOMPLETE" if missing else "REVIEW_REQUIRED" if invalid else "COMPLETE",
            "week_start": week.isoformat(), "preview": week != current_week,
            "evidence_cutoff": at.isoformat(), "column": prefix, "header_cell": prefix + str(header_row),
            "observed": observed, "missing": missing, "invalid": invalid,
            "computed_summary": summary_check,
            "scope": "Required weekly cells; shared comments and other sections need content review"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--at", help="ISO timestamp with timezone; defaults to now")
    parser.add_argument("--week-start", help="Explicit report week (YYYY-MM-DD) for a user-requested preview")
    args = parser.parse_args()
    try:
        context = json.loads(Path(args.context).read_text(encoding="utf-8-sig"))
        snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8-sig"))
        at = datetime.fromisoformat(args.at.replace("Z", "+00:00")) if args.at else datetime.now(timezone.utc)
        result = check(context, snapshot, at, args.week_start)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        result = {"status": "UNVERIFIED", "reason": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
