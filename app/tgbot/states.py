from aiogram.fsm.state import State, StatesGroup


class ViewCalendar(StatesGroup):
    view = State()
