import logging

from aiogram import Dispatcher

from app.models.config.main import BotConfig, Config
from app.tgbot import dialogs
from app.tgbot.handlers.base import setup_base
from app.tgbot.handlers.errors import setup_errors
from app.tgbot.handlers.superuser import setup_superuser

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, config: Config) -> None:
    setup_errors(dp, config.bot.log_chat)
    dp.include_router(setup_base())
    dp.include_router(setup_superuser(config.bot))
    dp.include_router(dialogs.setup(config))
    logger.debug("handlers configured successfully")
