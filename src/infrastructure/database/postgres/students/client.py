from typing import Optional
from sqlalchemy import select, update, delete, or_

from src.domain.students.schema import StudentsModel
from src.infrastructure.database.postgres.models import Students
from src.infrastructure.database.postgres.session_manager import AsyncSessionManager


class StudentsTable:

	def __init__(self) -> None:
		self.async_session = AsyncSessionManager()


	async def insert_student(self, username: str, password: str, class_id: int) -> int:
		async with self.async_session.get_session_begin() as session:
			insert_into = Students(username=username, password=password, class_id=class_id)

			session.add(insert_into)
			await session.flush()

			await session.refresh(insert_into)

			return insert_into.id


	async def select_students(self, username: Optional[str] = None, class_id: Optional[int] = None
							  ) -> list[StudentsModel] | StudentsModel:
		async with self.async_session.get_session() as session:

			if username is not None:
				select_student = select(Students).where(username == Students.username)
				student = await session.execute(select_student)

				return student.scalars().first()

			elif class_id is not None:
				select_student = select(Students).where(class_id == Students.class_id)
				student = await session.execute(select_student)

				return student.scalars().all()

			select_students = select(Students)
			all_students = await session.execute(select_students)

			return all_students.scalars().all()



	async def select_students_like(self, search_value: Optional[str] = None) -> list[StudentsModel]:
		async with self.async_session.get_session() as session:
			select_students = select(Students)

			if search_value is not None:
				select_students = select_students.where(
					or_(
						Students.username.like(f"%{search_value}%"),
						Students.firstname.like(f"%{search_value}%"),
						Students.lastname.like(f"%{search_value}%")
					)
				)

			result = await session.execute(select_students)
			return result.scalars().all()


	async def delete_student_by_username(self, username: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
			delete_student = delete(Students).where(username == Students.username)
			result = await session.execute(delete_student)

			await session.commit()

			if result.rowcount > 0:
				return True


	async def update_student_info(self, username: str, password: str, student_info: StudentsModel) -> bool | None:
		async with self.async_session.get_session_begin() as session:
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


	async def update_student_username(self, username: str, password: str, new_username: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
			update_student = update(Students).where(
				username == Students.username, password == Students.password
			).values(username=new_username)

			result = await session.execute(update_student)
			await session.commit()

			if result.rowcount > 0:
				return True


	async def update_student_password(self, username: str, password: str, new_password: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
			update_student = update(Students).where(
				username == Students.username, password == Students.password
			).values(password=new_password)

			result = await session.execute(update_student)
			await session.commit()

			if result.rowcount > 0:
				return True

