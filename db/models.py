from sqlalchemy import BigInteger, String, ForeignKey, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///habit.sqlite3')

async_sessionmaker = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass



class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
        
    habits: Mapped[list["Habit"]] = relationship("Habit", back_populates="user", cascade="all, delete-orphan")

    
    

class Habit(Base):
    __tablename__ = 'habits'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="habits")
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)