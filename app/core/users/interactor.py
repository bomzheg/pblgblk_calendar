from dataclasses import dataclass

from app.core.users import entity
from app.core.users.interfaces import UsersReader, UsersUpserter


@dataclass
class GetUsersInteractor:
    dao: UsersReader

    async def __call__(self) -> list[entity.User]:
        return await self.dao.get_users()



async def upsert_user(user: entity.CreateUserData, user_dao: UsersUpserter) -> entity.User:
    saved_user = await user_dao.upsert_user(user)
    await user_dao.commit()
    return saved_user
