from aiogram import F, Router
from aiogram.enums import ChatType

from . import base, view


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.include_router(base.setup())
    router.include_router(view.setup())
    return router
