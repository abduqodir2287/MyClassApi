from typing import Optional
from sqlalchemy import select, update

from src.domain.students.schema import StudentsModel
from src.infrastructure.database.postgres.database import Base
from src.infrastructure.database.postgres.models import Students

class StudentsTable:

	def __init__(self) -> None:
		self.async_session = Base.async_session


	async def insert_student(self, username: str, password: str) -> int:
		async with self.async_session() as session:
			async with session.begin():
				insert_into = Students(username=username, password=password)

				session.add(insert_into)
			await session.commit()

			await session.refresh(insert_into)

			return insert_into.id


	async def select_students(self, username: Optional[str] = None) -> list[StudentsModel] | StudentsModel:
		async with self.async_session() as session:

			if username is not None:

				select_student = select(Students).where(username == Students.username)
				student = await session.execute(select_student)

				return student.scalars().first()

			select_students = select(Students)
			all_students = await session.execute(select_students)

			return all_students.scalars().all()


	async def update_student_info(self, username: str, password: str, student_info: StudentsModel) -> bool | None:
		async with self.async_session() as session:
			async with session.begin():
				update_student = update(Students).where(
					username == Students.username, password == Students.password
				).values(
					firstname=student_info.firstname, lastname=student_info.lastname,
					birthDate=student_info.birthDate.date if student_info.birthDate is not None else None,
					age=student_info.age, gender=student_info.gender, subject=student_info.subject,
					interests=student_info.interests, idol=student_info.idol, bio=student_info.bio,
					social_link=student_info.social_link
				)

				result = await session.execute(update_student)
				await session.commit()

				if result.rowcount > 0:
					return True


