import datetime
from calendar import monthrange
from dataclasses import dataclass
from datetime import date


@dataclass(kw_only=True, slots=True)
class BusyDay:
    id: int
    _date: date
    is_busy: bool

    def flip(self) -> None:
        self.is_busy = not self.is_busy

    @property
    def date(self) -> datetime.date:
        return self._date


@dataclass(frozen=True, slots=True, kw_only=True)
class DateRange:
    start: date
    end: date

    def previous_month(self) -> "DateRange":
        return self.create_month(self.start - datetime.timedelta(days=1))

    def next_month(self) -> "DateRange":
        return self.create_month(self.end + datetime.timedelta(days=1))

    def __repr__(self) -> str:
        return f"{self.start.isoformat()}-{self.end.isoformat()}"

    @classmethod
    def create_month(cls, date_: date) -> "DateRange":
        _, last = monthrange(date_.year, date_.month)
        return cls(
            start=date_.replace(day=1),
            end=date_.replace(day=last),
        )

    @classmethod
    def create_this_month(cls) -> "DateRange":
        today = datetime.datetime.now(tz=datetime.UTC).date()
        return cls.create_month(today)

