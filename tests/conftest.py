import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src import main


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=main.app), base_url="http://test") as client:
        yield client

