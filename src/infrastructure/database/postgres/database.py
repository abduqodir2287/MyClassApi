from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.configs.config import get_settings


class Base(DeclarativeBase):
	pass


engine = create_async_engine(get_settings().DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)

