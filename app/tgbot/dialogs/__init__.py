from aiogram import Router

from . import edit_calendar, starters, view_calendar


def setup() -> Router:
    router = Router(name=__name__)
    router.include_router(starters.setup())
    router.include_router(view_calendar.setup())
    router.include_router(edit_calendar.setup())
    return router
