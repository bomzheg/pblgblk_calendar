from aiogram.fsm.state import StatesGroup, State


class ViewCalendar(StatesGroup):
    view = State()
