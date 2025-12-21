from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCalendar
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.identity import IdentityProvider
from app.core.plaining.interactors import FlipDayBusyInteractor


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
