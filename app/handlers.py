from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from db.models import async_sessionmaker, Habit, User
from aiogram.fsm.context import FSMContext
from app.fsm.state import HabitForm, DeleteHabit
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.keyboards as kb
import db.requests as rq

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
   await rq.set_user(message.from_user.id)
   await message.answer("Привет, я помогу тебе отслеживать привычки",
                        reply_markup=kb.menu)
   
@router.message(F.text == 'Добавить привычку')
async def new_habit(message: Message, state: FSMContext):
   await state.set_state(HabitForm.name)
   await message.answer('Введите название привычки')
   
@router.message(HabitForm.name)
async def procces_habit(message: Message, state: FSMContext):
   data = message.text
   async with async_sessionmaker() as session:  
      session.add(Habit(name=data, user_id=message.from_user.id))
      await session.commit()
   
   await message.answer(f'Привычка {message.text} успешно добавлена!')
   await state.clear()
   
@router.message(F.text == 'Мои привычки')
async def my_habits(message: Message):
   keyboard = await kb.habits(user_id=message.from_user.id)
   if not keyboard:
      await message.answer('У вас пока нет привычек')
      return
   
   await message.answer(
      'Ваши привычки:\n\nНажмите на привычку, что бы удалить.',
      reply_markup=keyboard
   )
   
   
@router.callback_query(F.data.startswith("delete_habit_"))
async def ask_confirm_delete(callback: CallbackQuery, state: FSMContext):
    habit_id = int(callback.data.split("_")[-1])
    
    async with async_sessionmaker() as session:
        habit = await session.get(Habit, habit_id)
        if not habit or habit.user_id != callback.from_user.id:
            await callback.answer("Привычка не найдена!")
            return
        
        await state.update_data(habit_id=habit_id, habit_name=habit.name)
        
        
        await callback.message.edit_text(
            f"Вы уверены, что хотите удалить привычку '{habit.name}'?",
            reply_markup=kb.confirim_delete.as_markup()
        )
        await state.set_state(DeleteHabit.confirm_delete)

@router.callback_query(F.data == "confirm_delete", DeleteHabit.confirm_delete)
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    async with async_sessionmaker() as session:
        await session.execute(
            rq.delete(Habit).where(Habit.id == data["habit_id"])
        )
        await session.commit()
    
    await callback.message.edit_text(
        f"Привычка '{data['habit_name']}' удалена!",
        reply_markup=None
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "cancel_delete", DeleteHabit.confirm_delete)
async def cancel_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Удаление отменено",
        reply_markup=None
    )
    await state.clear()
    await callback.answer()