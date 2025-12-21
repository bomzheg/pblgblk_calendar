from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory

from app.tgbot.services.identity import TgBotIdentityProvider


class LoadDataMiddleware(BaseMiddleware):
    def __init__(self, bg_manager: BgManagerFactory) -> None:
        self.bg_manager = bg_manager

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        dishka = data["dishka_container"]
        identity_provider = await dishka.get(TgBotIdentityProvider)

        data["user"] = await identity_provider.get_user()
        data["chat"] = await identity_provider.get_chat()
        data["bg_manager"] = self.bg_manager
        return await handler(event, data)
