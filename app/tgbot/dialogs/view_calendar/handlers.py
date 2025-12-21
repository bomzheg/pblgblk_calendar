from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.tgbot import states


async def select_user(_: CallbackQuery, __: Any, manager: DialogManager, user_id: str) -> None:
    data = manager.dialog_data
    data["user_id"] = int(user_id)
    await manager.switch_to(states.ViewCalendar.view)
