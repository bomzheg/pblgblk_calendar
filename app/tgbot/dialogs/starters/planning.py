from aiogram import Router
from aiogram.filters import Command

from app.tgbot import states
from app.tgbot.utils.router import register_start_handler


def setup() -> Router:
    router = Router(name=__name__)
    register_start_handler(
        Command(commands="view"),
        state=states.ViewCalendar.view,
        router=router,
    )
    register_start_handler(
        Command(commands="edit"),
        state=states.EditCalendar.edit,
        router=router,
    )
    return router
