from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory

from .data_load_middleware import LoadDataMiddleware


def setup_middlewares(dp: Dispatcher, bg_manager: BgManagerFactory) -> None:
    dp.message.middleware(LoadDataMiddleware(bg_manager))
