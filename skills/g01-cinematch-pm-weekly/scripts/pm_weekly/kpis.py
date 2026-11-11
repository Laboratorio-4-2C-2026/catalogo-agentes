import csv
import io
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from . import github

PRODUCTION = "prod"
DAILY_KPI_CAP = 10
DATA_FOLDER = "data"


@dataclass(frozen=True)
class GradingWindow:
    starts_on: date
    ends_on: date
    iso_weekdays: frozenset[int]
    timezone: str

    def graded_days_until(self, last_day: date) -> list[date]:
        days = []
        day = self.starts_on
        while day <= min(self.ends_on, last_day):
            if day.isoweekday() in self.iso_weekdays:
                days.append(day)
            day += timedelta(days=1)
        return days


@dataclass(frozen=True)
class CatalogEntry:
    kpi_id: str
    created_at: datetime
    deprecated_at: datetime | None

    def is_active_on(self, day: date, zone: ZoneInfo) -> bool:
        created_by_then = self.created_at.astimezone(zone).date() <= day
        deprecated_before = self.deprecated_at is not None and self.deprecated_at.astimezone(zone).date() <= day
        return created_by_then and not deprecated_before


@dataclass(frozen=True)
class Measurement:
    kpi_id: str
    received_at: datetime


@dataclass(frozen=True)
class DayCompliance:
    day: date
    received_kpis: frozenset[str]
    expected_kpis: frozenset[str]

    @property
    def grade(self) -> int:
        return min(len(self.received_kpis), DAILY_KPI_CAP)

    @property
    def missing_kpis(self) -> list[str]:
        return sorted(self.expected_kpis - self.received_kpis)

    @property
    def is_complete(self) -> bool:
        return bool(self.expected_kpis) and not self.missing_kpis


def fetch_compliance(repository: str, ref: str, *, project_id: str, until: date) -> tuple[GradingWindow, list[DayCompliance]]:
    window = parse_window(github.raw_file(repository, "settings.csv", ref=ref))
    catalog = parse_catalog(github.raw_file(repository, "catalog.csv", ref=ref), project_id=project_id)
    measurements = [
        measurement
        for file_name in _measurement_files(repository, ref, window, until=until)
        for measurement in parse_measurements(
            github.raw_file(repository, f"{DATA_FOLDER}/{file_name}", ref=ref), project_id=project_id
        )
    ]
    return window, daily_compliance(window, catalog, measurements, until=until)


def _measurement_files(repository: str, ref: str, window: GradingWindow, *, until: date) -> list[str]:
    """One CSV per value date; a value can arrive days after its date, so every file from the window start is read."""
    return [
        file_name
        for file_name in github.directory_entries(repository, DATA_FOLDER, ref=ref)
        if file_name.endswith(".csv") and window.starts_on.isoformat() <= file_name[:10] <= until.isoformat()
    ]


def parse_window(settings_csv: str) -> GradingWindow:
    settings = next(csv.DictReader(io.StringIO(settings_csv)))
    return GradingWindow(
        starts_on=date.fromisoformat(settings["starts_on"]),
        ends_on=date.fromisoformat(settings["ends_on"]),
        iso_weekdays=frozenset(int(day) for day in settings["weekdays"].strip("{}").split(",")),
        timezone=settings["timezone"],
    )


def parse_catalog(catalog_csv: str, *, project_id: str) -> list[CatalogEntry]:
    return [
        CatalogEntry(
            kpi_id=row["id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            deprecated_at=datetime.fromisoformat(row["deprecated_at"]) if row["deprecated_at"] else None,
        )
        for row in csv.DictReader(io.StringIO(catalog_csv))
        if row["project_id"] == project_id and row["env"] == PRODUCTION
    ]


def parse_measurements(measurements_csv: str, *, project_id: str) -> list[Measurement]:
    return [
        Measurement(kpi_id=row["kpi_id"], received_at=datetime.fromisoformat(row["reported_at"]))
        for row in csv.DictReader(io.StringIO(measurements_csv))
        if row["project_id"] == project_id and row["env"] == PRODUCTION
    ]


def daily_compliance(
    window: GradingWindow,
    catalog: list[CatalogEntry],
    measurements: list[Measurement],
    *,
    until: date,
) -> list[DayCompliance]:
    """Graded by the day the platform received each value, in the platform's timezone, not by the value's own date."""
    zone = ZoneInfo(window.timezone)
    received_by_day: dict[date, set[str]] = {}
    for measurement in measurements:
        received_by_day.setdefault(measurement.received_at.astimezone(zone).date(), set()).add(measurement.kpi_id)
    return [
        DayCompliance(
            day=day,
            received_kpis=frozenset(received_by_day.get(day, set())),
            expected_kpis=frozenset(entry.kpi_id for entry in catalog if entry.is_active_on(day, zone)),
        )
        for day in window.graded_days_until(until)
    ]
