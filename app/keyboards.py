from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.models import Habit, User
from db.requests import get_habits

menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Добавить привычку'),
        KeyboardButton(text='Мои привычки')
    ] 
],
                           resize_keyboard=True)

async def habits(user_id):
    all_habits = await get_habits(user_id=user_id)
    if not all_habits:
        return None
    keyboard = InlineKeyboardBuilder()
    for habit in all_habits:
            keyboard.add(InlineKeyboardButton(
                text=habit.name,
                callback_data=f'delete_habit_{habit.id}'
            ))
    return keyboard.adjust(1).as_markup()
    
confirim_delete = InlineKeyboardBuilder()
confirim_delete.add(
    InlineKeyboardButton(text="✅ Да", callback_data="confirm_delete"),
    InlineKeyboardButton(text="❌ Нет", callback_data="cancel_delete")
)
