from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.configs.config import get_settings


class TestBase(DeclarativeBase):
	pass


test_engine = create_async_engine(get_settings().TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

