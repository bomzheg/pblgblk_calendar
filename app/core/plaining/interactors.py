from dataclasses import dataclass
from datetime import date

from app.core import users
from app.core.identity import IdentityProvider
from app.core.plaining import entity
from app.core.plaining.interfaces import BusyDayDao, BusyDaysReader


@dataclass
class FlipDayBusyInteractor:
    dao: BusyDayDao

    async def __call__(self, date_: date, identity: IdentityProvider) -> None:
        busy_date = await self.dao.get_busy_date(date_, await identity.get_required_user_id())
        busy_date.flip()
        await self.dao.save_busy_day(busy_date)
        await self.dao.commit()


@dataclass
class BusyDaysReaderInteractor:
    dao: BusyDaysReader

    async def __call__(
        self, date_range: entity.DateRange, user_id: users.UserId
    ) -> list[entity.BusyDay]:
        return await self.dao.get_only_busy_date(
            date_range=date_range,
            user_id=user_id,
        )
