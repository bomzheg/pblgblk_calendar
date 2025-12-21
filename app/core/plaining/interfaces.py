from datetime import date
from typing import Protocol

from app.core.plaining import entity
from app.models.dto.user import UserId


class BusyDayReader(Protocol):
    async def get_busy_date(self, date_: date, user_id: UserId) -> entity.BusyDay:
        raise NotImplementedError


class BusyDaysReader(Protocol):
    async def get_only_busy_date(
        self, date_range: entity.DateRange, user_id: UserId
    ) -> list[entity.BusyDay]:
        raise NotImplementedError


class BusyDayWriter(Protocol):
    async def save_busy_day(self, busy_day: entity.BusyDay) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError


class BusyDayDao(BusyDayReader, BusyDayWriter):
    pass
