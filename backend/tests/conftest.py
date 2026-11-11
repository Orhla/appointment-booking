import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database import Base, get_session
import uuid
from sqlalchemy import text
from sqlalchemy.engine import make_url
from app.config import get_settings
import app.models
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture(scope="session")
async def engine():
    server_url = make_url(get_settings().database_url)
    test_db = f"test_{uuid.uuid4().hex}"

    admin = create_async_engine(
        server_url.set(database="postgres"), isolation_level="AUTOCOMMIT"
    )
    async with admin.connect() as conn:
        await conn.execute(text(f'CREATE DATABASE "{test_db}"'))

    e = create_async_engine(server_url.set(database=test_db))
    try:
        async with e.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield e
    finally:
        await e.dispose()
        async with admin.connect() as conn:
            await conn.execute(text(f'DROP DATABASE "{test_db}" WITH (FORCE)'))
        await admin.dispose()

@pytest.fixture
async def session(engine):
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as s:
        yield s
        await s.rollback()

@pytest.fixture
async def client(session):
    
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()