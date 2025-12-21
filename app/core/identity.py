from typing import Protocol

from app.core import exceptions, users
from app.models import dto


class IdentityProvider(Protocol):
    async def get_user(self) -> users.User | None:
        raise NotImplementedError

    async def get_chat(self) -> dto.Chat | None:
        raise NotImplementedError

    async def get_required_user(self) -> users.User:
        user = await self.get_user()
        if user is None:
            raise exceptions.UserNotFound
        return user

    async def get_required_user_id(self) -> users.UserId:
        user = await self.get_required_user()
        return user.db_id

    async def get_required_chat(self) -> dto.Chat:
        chat = await self.get_chat()
        if chat is None:
            raise exceptions.ChatNotFound
        return chat
