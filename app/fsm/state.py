from aiogram.fsm.state import State, StatesGroup

class HabitForm(StatesGroup):
    name = State()

class DeleteHabit(StatesGroup):
    confirm_delete = State()