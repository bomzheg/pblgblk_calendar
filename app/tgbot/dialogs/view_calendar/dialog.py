from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from app.tgbot import states
from app.tgbot.dialogs.view_calendar.getters import get_busy_days
from app.tgbot.dialogs.widgets import BusyCalendar

view_calendar = Dialog(
    Window(
        Jinja("Календарь ниже"),
        BusyCalendar(id="view_calendar"),
        state=states.ViewCalendar.view,
        getter=get_busy_days,
    )
)
