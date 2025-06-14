from db.models import Habit, User
from db.models import async_sessionmaker
from sqlalchemy import select, update, delete, join

async def set_user(tg_id):
    async with async_sessionmaker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
  
async def get_habits(user_id):
    async with async_sessionmaker() as session:
        result = await session.execute(
            select(Habit).where(Habit.user_id == user_id)
        )
        return result.scalars().all()
        
    
async def delete_habit(habit_user_id):
    async with async_sessionmaker() as session:
        session.delete(select(Habit).where(Habit.id == habit_user_id))