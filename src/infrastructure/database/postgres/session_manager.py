from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from src.infrastructure.database.postgres.database import async_session



class AsyncSessionManager:

    def __init__(self) -> None:
        self.async_session = async_session


    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session


    @asynccontextmanager
    async def get_session_begin(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            async with session.begin():
                yield session


