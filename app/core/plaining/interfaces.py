from datetime import date
from io import BytesIO
from typing import Protocol

from app.core import users
from app.core.common import Commiter
from app.core.plaining import entity


class BusyDayReader(Protocol):
    async def get_busy_date(self, date_: date, user_id: users.UserId) -> entity.BusyDay:
        raise NotImplementedError


class BusyDaysReader(Protocol):
    async def get_only_busy_date(
        self, date_range: entity.DateRange, user_id: users.UserId
    ) -> list[entity.BusyDay]:
        raise NotImplementedError


class BusyDayWriter(Commiter, Protocol):
    async def save_busy_day(self, busy_day: entity.BusyDay) -> None:
        raise NotImplementedError


class BusyDayDao(BusyDayReader, BusyDayWriter):
    pass


class CalendarPainter(Protocol):
    def paint(self, year: int, month: int, dates: list[date]) -> BytesIO:
        raise NotImplementedError
