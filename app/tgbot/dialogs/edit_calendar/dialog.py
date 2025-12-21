from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from app.tgbot import states
from app.tgbot.dialogs.widgets import BusyCalendar

from .getters import get_busy_days
from .handlers import calendar_on_click

edit_calendar = Dialog(
    Window(
        Jinja("Это твой календарь, нажми на любой день чтобы пометить его занятым"),  # noqa: RUF001
        BusyCalendar(id="edit_calendar", on_click=calendar_on_click),  # type: ignore[arg-type]
        state=states.EditCalendar.edit,
        getter=get_busy_days,
    )
)
