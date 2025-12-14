
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Jinja

from app.tgbot import states

view_calendar = Dialog(
    Window(
        Jinja("Календарь ниже"),
        Calendar(id="view_calendar"),
        state=states.ViewCalendar.view
    )
)