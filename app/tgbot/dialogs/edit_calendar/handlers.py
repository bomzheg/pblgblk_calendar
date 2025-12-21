import datetime
from datetime import date
from typing import Any

from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from aiogram_dialog.widgets.kbd import ManagedCalendar
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.identity import IdentityProvider
from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import CalendarPainterInteractor, FlipDayBusyInteractor
from app.tgbot.dialogs.widgets import BusyCalendar


@inject
async def calendar_on_click(
    _: CallbackQuery,
    __: ManagedCalendar,
    ___: DialogManager,
    date_: date,
    interator: FromDishka[FlipDayBusyInteractor],
    identity: FromDishka[IdentityProvider],
) -> None:
    await interator(date_=date_, identity=identity)


@inject
async def paint_cal(
    callback_query: CallbackQuery,
    __: Any,
    dialog_manager: DialogManager,
    interactor: FromDishka[CalendarPainterInteractor],
    identity: FromDishka[IdentityProvider],
) -> None:
    view_calendar: ManagedWidget[BusyCalendar] = dialog_manager.find("edit_calendar")  # type: ignore[assignment]
    current = view_calendar.widget.get_offset(dialog_manager)
    if current is None:
        current = datetime.datetime.now(tz=datetime.UTC).date()
    cal = await interactor(
        date_range=DateRange.create_month(current), user_id=await identity.get_required_user_id()
    )
    assert callback_query.message  # noqa: S101
    await callback_query.message.answer_photo(
        photo=BufferedInputFile(file=cal.read(), filename="calendar.png")
    )
