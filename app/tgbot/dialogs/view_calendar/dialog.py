from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Jinja, Multi, Const

from app.tgbot import states
from app.tgbot.dialogs.widgets import BusyCalendar

from .getters import get_busy_days, get_users
from .handlers import select_user

view_calendar = Dialog(
    Window(
        Jinja("Выбери пользователя"),
        ScrollingGroup(
            Select(
                Jinja("{{item.name_mention}}"),
                id="calendar_users",
                item_id_getter=lambda x: x.db_id,
                items="users",
                on_click=select_user,
            ),
            id="users_sg",
            width=1,
            height=10,
        ),
        state=states.ViewCalendar.users,
        getter=get_users,
    ),
    Window(
        Jinja("Календарь ниже"),
        BusyCalendar(id="view_calendar"),
        state=states.ViewCalendar.view,
        getter=get_busy_days,
    )
)
