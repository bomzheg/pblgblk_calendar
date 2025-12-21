from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.sql.functions import user

from app.tgbot import states


async def select_user(c: CallbackQuery, widget: Any, manager: DialogManager, user_id: str):
    data = manager.dialog_data
    data["user_id"] = int(user_id)
    await manager.switch_to(states.ViewCalendar.view)
