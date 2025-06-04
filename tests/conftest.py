import asyncio
import pytest_asyncio


from httpx import ASGITransport, AsyncClient
from collections.abc import AsyncGenerator

from src.main import app
from src.infrastructure.database.postgres.database import engine, Base



@pytest_asyncio.fixture(scope="session")
async def prepare_test_db():
    async with engine.begin() as conn:
        print("📥 Создание всех таблиц для тестов")
        await conn.run_sync(Base.metadata.create_all)

    yield

    await asyncio.sleep(0.1)

    async with engine.begin() as conn:
        print("🧹 Удаление всех таблиц после тестов")
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

