from aiogram import Router, F
from aiogram.enums import ChatType

from . import stat, base


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.include_router(base.setup())
    router.include_router(stat.setup())
    return router
