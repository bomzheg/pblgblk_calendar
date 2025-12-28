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
from app.infrastructure.nursery import RequestNursery, inject_task
from app.models.config.main import BotConfig


@inject
async def send_calendar_inline(
    inline_query: InlineQuery,
    identity: FromDishka[IdentityProvider],
    nursery: FromDishka[RequestNursery],
) -> None:
    this_month = DateRange.create_this_month()
    previous_month = this_month.previous_month()
    next_month = this_month.next_month()
    user_db_id = await identity.get_required_user_id()

    tasks = [
        nursery(generate_and_send, date_range=previous_month, user_db_id=user_db_id),
        nursery(generate_and_send, date_range=this_month, user_db_id=user_db_id),
        nursery(generate_and_send, date_range=next_month, user_db_id=user_db_id),
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
    for msg in sent:
        nursery(delete_message, msg=msg)


@inject_task
async def delete_message(msg: Message, bot: FromDishka[Bot]) -> bool:
    return await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


@inject_task
async def generate_and_send(
    date_range: DateRange,
    user_db_id: users.UserId,
    interactor: FromDishka[CalendarPainterInteractor],
    bot: FromDishka[Bot],
    config: FromDishka[BotConfig],
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
