from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from src.infrastructure.database.postgres.database import Base


class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	role = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


