import datetime

from aiogram import Router, Bot
from aiogram.enums import InlineQueryResultType
from aiogram.handlers import InlineQueryHandler
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputMessageContent, InlineQueryResultPhoto, \
    BufferedInputFile, InlineQueryResultCachedPhoto, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.core import users
from app.core.identity import IdentityProvider
from app.core.plaining.entity import DateRange
from app.core.plaining.interactors import CalendarPainterInteractor
from app.models.config.main import BotConfig


@inject
async def send_calendar_inline(
    inline_query: InlineQuery,
    bot: Bot,
    interactor: FromDishka[CalendarPainterInteractor],
    identity: FromDishka[IdentityProvider],
    config: FromDishka[BotConfig],

):
    date_range = DateRange.create_this_month()
    result = await interactor(date_range=date_range, user_id=await identity.get_required_user_id())
    sent = await bot.send_photo(
        chat_id=inline_query.from_user.id,
        photo=BufferedInputFile(file=result.read(), filename="calendar.png"),
        disable_notification=True,
    this_month = DateRange.create_this_month()

    sent = await generate_and_send(
        date_range=this_month,
        interactor=interactor,
        user_db_id=await identity.get_required_user_id(),
        bot=bot,
        config=config,
    )
    result = [
        InlineQueryResultCachedPhoto(
            type=InlineQueryResultType.PHOTO,
            id=repr(this_month),
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


async def generate_and_send(
    date_range: DateRange,
    interactor: CalendarPainterInteractor,
    user_db_id: users.UserId,
    bot: Bot,
    config: BotConfig
) -> Message:
    data_cal = await interactor(date_range=date_range, user_id=user_db_id)
    return await bot.send_photo(
        chat_id=config.log_chat,
        photo=BufferedInputFile(file=data_cal.read(), filename="calendar.png"),
        disable_notification=True,
    )

def setup() -> Router:
    router = Router(name=__name__)
    router.inline_query.register(send_calendar_inline)
    return router
