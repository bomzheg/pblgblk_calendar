from datetime import date

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.plaining import entity
from app.dao.base import BaseDAO
from app.models.db.busy_day import BusyDay
from app.models.dto import UserId


class BusyDayDAO(BaseDAO[BusyDay]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BusyDay, session)

    async def get_busy_date(self, date_: date, user_id: UserId) -> entity.BusyDay:
        kwargs = {
            "user_id": user_id,
            "date": date_,
        }
        saved = await self.session.execute(
            insert(BusyDay)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(BusyDay.user_id, BusyDay.date_),
                set_=kwargs,
                where=(BusyDay.user_id == user_id) and (BusyDay.date_ == date_),
            )
            .returning(BusyDay)
        )
        return saved.scalar_one().to_dto()

    async def save_busy_day(self, busy_day: entity.BusyDay) -> None:
        await self.session.execute(
            update(BusyDay).where(BusyDay.id == busy_day.id).values(busy=busy_day.is_busy)
        )
