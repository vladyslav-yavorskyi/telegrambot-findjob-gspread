from aiogram.fsm.state import StatesGroup, State


class Info(StatesGroup):
    phone_number = State()
    is_looking = State()
    name = State()
    job = State()
