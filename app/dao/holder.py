from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import ChatDAO, UserDAO
from app.dao.busy_day import BusyDayDAO


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDAO = field(init=False)
    chat: ChatDAO = field(init=False)
    busy_day: BusyDayDAO = field(init=False)

    def __post_init__(self) -> None:
        self.user = UserDAO(self.session)
        self.chat = ChatDAO(self.session)
        self.busy_day = BusyDayDAO(self.session)

    async def commit(self) -> None:
        await self.session.commit()
