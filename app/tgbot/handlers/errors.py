import json
import logging
from functools import partial

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd
from aiogram_dialog.api.exceptions import UnknownIntent

logger = logging.getLogger(__name__)


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot) -> None:
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error.exception.__class__.__name__,
        error.update.dict(exclude_none=True),
        exc_info=error.exception,
    )
    if not log_chat_id:
        return
    await bot.send_message(
        log_chat_id,
        f"Received exception {hd.quote(str(error.exception))}\n"
        f"by processing update "
        f"{hd.quote(json.dumps(error.update.dict(exclude_none=True), default=str)[:3500])}\n",
    )

async def clear_unknown_intent(error: ErrorEvent, bot: Bot):
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


def setup_errors(dp: Dispatcher, log_chat_id: int) -> None:
    dp.errors.register(clear_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dp.errors.register(partial(handle, log_chat_id=log_chat_id))
