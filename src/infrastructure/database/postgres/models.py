from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from src.infrastructure.database.postgres.database import Base


class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	role = Column(String, nullable=False)
	photo_url = Column(String, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Class(Base):
	__tablename__ = "class"
	id = Column(Integer, primary_key=True)
	class_name = Column(String, nullable=False)
	students_count = Column(Integer, nullable=False)
	teacher_username = Column(String, ForeignKey("teachers.username"))
	school_year = Column(String, nullable=False)
	class_leader_username = Column(String, nullable=True)
	class_photo_url = Column(String, nullable=True)
	description = Column(String, nullable=True)
	class_room_number = Column(Integer, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

	students = relationship("Students", back_populates="class_info")
	teacher = relationship("Teachers", back_populates="classes")


class Students(Base):
	__tablename__ = "students"
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	class_id = Column(Integer, ForeignKey("class.id"))
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

	class_info = relationship("Class", back_populates="students")


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
	gender = Column(String, nullable=True)
	subject = Column(String, nullable=True)
	idol = Column(String, nullable=True)
	bio = Column(String, nullable=True)
	social_link = Column(String, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
	updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

	classes = relationship("Class", back_populates="teacher")


