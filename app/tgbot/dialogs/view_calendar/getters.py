import datetime
from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.core.identity import IdentityProvider
from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import BusyDaysReaderInteractor
from app.tgbot.dialogs.widgets import ViewCalendar


@inject
async def get_forbidden(
    reader: FromDishka[BusyDaysReaderInteractor],
    identity: FromDishka[IdentityProvider],
    dialog_manager: DialogManager,
    **_,  # noqa: ANN003
) -> dict[str, Any]:
    view_calendar: ManagedWidget[ViewCalendar] = dialog_manager.find("view_calendar")  # type: ignore[assignment]
    current = view_calendar.widget.get_offset(dialog_manager)
    if current is None:
        current = datetime.datetime.now(tz=datetime.UTC).date()
    busy_days = await reader(
        date_range=DateRange.create_month(current),
        # TODO we want to show for selected user, not for everyone
        user_id=await identity.get_required_user_id(),
    )
    return {"forbidden": [d.date for d in busy_days]}
