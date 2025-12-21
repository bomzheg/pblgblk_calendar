from aiogram import Router
from aiogram.filters import Command

from app.models.config import Config
from app.tgbot import states
from app.tgbot.utils.router import register_start_handler


def setup(config: Config) -> Router:
    router = Router(name=__name__)
    register_start_handler(
        Command(commands="view"),
        state=states.ViewCalendar.users,
        router=router,
    )
    register_start_handler(
        Command(commands="edit"),
        state=states.EditCalendar.edit,
        router=router,
    )
    register_start_handler(
        Command(commands=["main", "pblgblk"]),
        state=states.ViewCalendar.view,
        router=router,
        data={"user_tg_id": config.primary_user_id}
    )
    return router
