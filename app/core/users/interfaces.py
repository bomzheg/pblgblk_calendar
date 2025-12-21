from typing import Protocol

from app.core.common import Commiter
from app.core.users import entity


class UsersReader(Protocol):
    async def get_users(self) -> list[entity.User]:
        raise NotImplementedError


class UsersUpserter(Commiter, Protocol):
    async def upsert_user(self, user: entity.CreateUserData) -> entity.User:
        raise NotImplementedError

class UserFinder(Protocol):
    async def get_by_tg_id(self, tg_id: int) -> entity.User:
        raise NotImplementedError
