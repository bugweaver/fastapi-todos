from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

engine = create_async_engine("sqlite+aiosqlite:///todo.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
test_session = async_sessionmaker(test_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


async def create_test_db_and_tables():  # Функция для создания таблиц в ТЕСТОВОЙ БД
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
