import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.database import Base
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TEST_DATABASE_URL = getenv("TEST_DATABASE_URL")

@pytest.fixture(scope="session")
async def engine():
    e = create_async_engine(TEST_DATABASE_URL)
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield e
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await e.dispose()

@pytest.fixture
async def session(engine):
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as s:
        yield s
        await s.rollback()