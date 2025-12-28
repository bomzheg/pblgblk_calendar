import datetime

from aiogram import Router, Bot
from aiogram.enums import InlineQueryResultType
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputMessageContent, InlineQueryResultPhoto, \
    BufferedInputFile, InlineQueryResultCachedPhoto
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.core.identity import IdentityProvider
from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import CalendarPainterInteractor


@inject
async def send_calendar_inline(
    inline_query: InlineQuery,
    bot: Bot,
    interactor: FromDishka[CalendarPainterInteractor],
    identity: FromDishka[IdentityProvider],

):
    date_range = DateRange.create_this_month()
    result = await interactor(date_range=date_range, user_id=await identity.get_required_user_id())
    sent = await bot.send_photo(
        chat_id=inline_query.from_user.id,
        photo=BufferedInputFile(file=result.read(), filename="calendar.png"),
        disable_notification=True,
    )
    result = [
        InlineQueryResultCachedPhoto(
            type=InlineQueryResultType.PHOTO,
            id=repr(date_range),
            photo_file_id=sent.photo[-1].file_id,
            title="Мой календарь",
            description="Этот месяц",
        )
    ]
    await inline_query.answer(
        results=result,  # type: ignore[arg-type]
        is_personal=True,
        cache_time=30,
    )
    await sent.delete()


def setup() -> Router:
    router = Router(name=__name__)
    router.inline_query.register(send_calendar_inline)
    return router
