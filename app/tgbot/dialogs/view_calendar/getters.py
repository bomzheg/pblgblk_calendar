import datetime
from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.identity import IdentityProvider
from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import BusyDaysReaderInteractor
from app.core.users.interactor import GetUsersInteractor
from app.tgbot.dialogs.widgets import BusyCalendar


@inject
async def get_busy_days(
    reader: FromDishka[BusyDaysReaderInteractor],
    identity: FromDishka[IdentityProvider],
    dialog_manager: DialogManager,
    **_,  # noqa: ANN003
) -> dict[str, Any]:
    view_calendar: ManagedWidget[BusyCalendar] = dialog_manager.find("view_calendar")  # type: ignore[assignment]
    current = view_calendar.widget.get_offset(dialog_manager)
    if current is None:
        current = datetime.datetime.now(tz=datetime.UTC).date()
    busy_days = await reader(
        date_range=DateRange.create_month(current),
        user_id=dialog_manager.dialog_data["user_id"],
    )
    return {"busy": [d.date for d in busy_days]}


@inject
async def get_users(
    interactor: FromDishka[GetUsersInteractor],
    **_,  # noqa: ANN003
):
    return {
        "users": await interactor()
    }