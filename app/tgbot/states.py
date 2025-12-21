from aiogram.fsm.state import State, StatesGroup


class ViewCalendar(StatesGroup):
    users = State()
    view = State()


class EditCalendar(StatesGroup):
    edit = State()
