from aiogram import Router

from .dialog import view_calendar


def setup() -> Router:
    router = Router(name=__name__)
    router.include_router(view_calendar)
    return router
