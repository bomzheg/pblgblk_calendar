from aiogram import Router, F
from aiogram.enums import ChatType

from . import view, base


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.include_router(base.setup())
    router.include_router(view.setup())
    return router
