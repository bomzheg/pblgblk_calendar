from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.users.interactor import UserByTgIdFinder
from app.tgbot import states


async def select_user(_: CallbackQuery, __: Any, manager: DialogManager, user_id: str) -> None:
    data = manager.dialog_data
    data["user_id"] = int(user_id)
    await manager.switch_to(states.ViewCalendar.view)


@inject
async def on_start_view(
    data: dict[str, Any],
    manager: DialogManager,
    interactor: FromDishka[UserByTgIdFinder],
) -> None:
    if data and "user_tg_id" in data:
        user = await interactor(data["user_tg_id"])
        manager.dialog_data["user_id"] = user.db_id
