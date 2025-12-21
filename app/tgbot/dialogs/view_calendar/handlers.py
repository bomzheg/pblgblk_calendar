import datetime
from typing import Any

from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import CalendarPainterInteractor
from app.core.users.interactor import UserByTgIdFinder
from app.tgbot import states
from app.tgbot.dialogs.widgets import BusyCalendar


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


@inject
async def paint_cal(
    callback_query: CallbackQuery,
    __: Any,
    dialog_manager: DialogManager,
    interactor: FromDishka[CalendarPainterInteractor],
) -> None:
    view_calendar: ManagedWidget[BusyCalendar] = dialog_manager.find("view_calendar")  # type: ignore[assignment]
    current = view_calendar.widget.get_offset(dialog_manager)
    if current is None:
        current = datetime.datetime.now(tz=datetime.UTC).date()
    cal = await interactor(
        date_range=DateRange.create_month(current), user_id=dialog_manager.dialog_data["user_id"]
    )
    assert callback_query.message  # noqa: S101
    await callback_query.message.answer_photo(
        photo=BufferedInputFile(file=cal.read(), filename="calendar.png")
    )
