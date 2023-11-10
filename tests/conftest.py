import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.core.base import Base
from src.db.db import get_session
from src.main import app

metadata = Base.metadata


class SettingsTest(BaseSettings):
    """Настройки тестовой базы данных"""
    db_host_test: str
    db_port_test: int
    db_name_test: str
    db_user_test: str
    db_pass_test: str

    class Config:
        env_file = '.env'


settings_test = SettingsTest()


# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{settings_test.db_user_test}:{settings_test.db_pass_test}@{settings_test.db_host_test}:{settings_test.db_port_test}/{settings_test.db_name_test}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(metadata.drop_all)

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
def test_user():
    return {"username": "user@example.com", "password": "string"}
