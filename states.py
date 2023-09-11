from aiogram.fsm.state import StatesGroup, State


class Info(StatesGroup):
    job_search_target = State()
    name = State()
    phone = State()
    is_correct = State()
    name_update = State()
    phone_update = State()
    job_search_target_update = State()
