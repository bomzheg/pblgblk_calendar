import asyncio
from functools import partial

from aiogram import Bot, Router
from aiogram.enums import InlineQueryResultType
from aiogram.types import (
    BufferedInputFile,
    InlineQuery,
    InlineQueryResultCachedPhoto,
    Message,
)
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
) -> None:
    this_month = DateRange.create_this_month()
    previous_month = this_month.previous_month()
    next_month = this_month.next_month()
    generator = partial(
        generate_and_send,
        interactor=interactor,
        user_db_id=await identity.get_required_user_id(),
        bot=bot,
        config=config,
    )

    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(generator(date_range=previous_month)),
            group.create_task(generator(date_range=this_month)),
            group.create_task(generator(date_range=next_month)),
        ]
        sent = [await task for task in tasks]
        result = [
            InlineQueryResultCachedPhoto(
                type=InlineQueryResultType.PHOTO,
                id=repr(previous_month),
                photo_file_id=sent[0].photo[-1].file_id,  # type: ignore[index]
                title="Мой календарь",
                description="Предыдущий месяц",
            ),
            InlineQueryResultCachedPhoto(
                type=InlineQueryResultType.PHOTO,
                id=repr(this_month),
                photo_file_id=sent[1].photo[-1].file_id,  # type: ignore[index]
                title="Мой календарь",
                description="Этот месяц",
            ),
            InlineQueryResultCachedPhoto(
                type=InlineQueryResultType.PHOTO,
                id=repr(next_month),
                photo_file_id=sent[2].photo[-1].file_id,  # type: ignore[index]
                title="Мой календарь",
                description="Следующий месяц",
            ),
        ]
        await inline_query.answer(
            results=result,  # type: ignore[arg-type]
            is_personal=True,
            cache_time=30,
        )
        delete_tasks = [
            group.create_task(bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id))
            for msg in sent
        ]
        for task in delete_tasks:
            await task


async def generate_and_send(
    date_range: DateRange,
    interactor: CalendarPainterInteractor,
    user_db_id: users.UserId,
    bot: Bot,
    config: BotConfig,
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
