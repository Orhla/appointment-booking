from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from os import getenv
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = getenv("DATABASE_DOCKER_URL")

if not DATABASE_URL:
    raise RuntimeError("Критическая ошибка: Переменная окружения DATABASE_DOCKER_URL не задана!")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session