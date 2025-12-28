import logging

from aiogram import Dispatcher

from app.models.config.main import Config
from app.tgbot import dialogs

from . import base, errors, inline, superuser

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, config: Config) -> None:
    errors.setup_errors(dp, config.bot.log_chat)
    dp.include_router(base.setup_base())
    dp.include_router(superuser.setup_superuser(config.bot))
    dp.include_router(inline.setup())
    dp.include_router(dialogs.setup(config))
    logger.debug("handlers configured successfully")
