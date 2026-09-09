from aiogram.fsm.state import State, StatesGroup
class RegMaxState(StatesGroup):
    Phone = State()
    Code = State()
