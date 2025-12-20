
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Jinja

from app.tgbot import states
from app.tgbot.dialogs.view_calendar.getters import get_forbidden
from app.tgbot.dialogs.widgets import ViewCalendar

view_calendar = Dialog(
    Window(
        Jinja("Календарь ниже"),
        ViewCalendar(id="view_calendar"),
        state=states.ViewCalendar.view,
        getter=get_forbidden
    )
)