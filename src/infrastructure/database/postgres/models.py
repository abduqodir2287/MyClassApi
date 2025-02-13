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


class Students(Base):
	__tablename__ = "students"
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	firstname = Column(String, nullable=True)
	lastname = Column(String, nullable=True)
	photo_url = Column(String, nullable=True)
	birthDate = Column(String, nullable=True)
	age = Column(Integer, nullable=True)
	gender = Column(String, nullable=True)
	subject = Column(String, nullable=True)
	interests = Column(String, nullable=True)
	idol = Column(String, nullable=True)
	bio = Column(String, nullable=True)
	social_link = Column(String, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Teachers(Base):
	__tablename__ = "teachers"
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	firstname = Column(String, nullable=True)
	lastname = Column(String, nullable=True)
	photo_url = Column(String, nullable=True)
	birthDate = Column(String, nullable=True)
	age = Column(Integer, nullable=True)
	subject = Column(String, nullable=True)
	idol = Column(String, nullable=True)
	bio = Column(String, nullable=True)
	social_link = Column(String, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


