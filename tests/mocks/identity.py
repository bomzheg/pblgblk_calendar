from dataclasses import dataclass

from app.core.identity import IdentityProvider
from app.models import dto


@dataclass(kw_only=True)
class MockIdentityProvider(IdentityProvider):
    user: dto.User | None = None
    chat: dto.Chat | None = None

    async def get_chat(self) -> dto.Chat | None:
        return self.chat

    async def get_user(self) -> dto.User | None:
        return self.user
