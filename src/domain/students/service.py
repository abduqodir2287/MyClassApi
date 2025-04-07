from typing import Optional
from fastapi import HTTPException, status

from src.configs.logger_setup import logger
from src.domain.students.schema import StudentsModel
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.domain.enums import Gender
from src.domain.schema import Date

class StudentsRouterService:

	def __init__(self) -> None:
		self.students_table = StudentsTable()


	async def get_all_students_service(self) -> list[StudentsModel]:
		students_list = []

		for student in await self.students_table.select_students():

			returned_student = StudentsModel(
				id=student.id, username=student.username, firstname=student.firstname, lastname=student.lastname,
				birthDate=Date(date=student.birthDate) if student.birthDate is not None else student.birthDate, # type: ignore
				age=student.age, gender=student.gender, subject=student.subject, interests=student.interests,
				idol=student.idol, created_at=student.created_at, updated_at=student.updated_at
			)

			students_list.append(returned_student)

		return students_list



	async def get_student_by_username_service(self, username: str) -> StudentsModel:
		get_student = await self.students_table.select_students(username=username)

		if not get_student:
			logger.warning("Student not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with this username not found")

		return StudentsModel(
				id=get_student.id, username=get_student.username, firstname=get_student.firstname, lastname=get_student.lastname,
				birthDate=Date(date=get_student.birthDate) if get_student.birthDate is not None else get_student.birthDate, # type: ignore
				age=get_student.age, gender=get_student.gender, subject=get_student.subject, interests=get_student.interests,
				idol=get_student.idol, created_at=get_student.created_at, updated_at=get_student.updated_at
			)



	async def update_student_service(
			self, username: str, password: str, firstname: Optional[str] = None,
			lastname: Optional[str] = None, birth_date: Optional[Date] = None, age: Optional[int] = None,
			gender: Optional[Gender] = None, subject: Optional[str] = None, interests: Optional[str] = None,
			idol: Optional[str] = None, bio: Optional[str] = None, social_link: Optional[str] = None
	) -> StudentsModel | None:
		user_info = await self.students_table.select_students(username=username)

		if not user_info:
			logger.warning("Student not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with this username not found")

		if birth_date is None and user_info.birthDate is not None:
			birth_date = Date(date=user_info.birthDate) # type: ignore

		elif birth_date is None and user_info.birthDate is None:
			birth_date = None

		student_model = StudentsModel(
			id=user_info.id, username=user_info.username, firstname=firstname if firstname is not None else user_info.firstname,
			lastname=lastname if lastname is not None else user_info.lastname, birthDate=birth_date,
			age=age if age is not None else user_info.age, gender=gender if gender is not None else user_info.gender,
			subject=subject if subject is not None else user_info.subject,
			interests=interests if interests is not None else user_info.interests,
			idol=idol if idol is not None else user_info.idol, bio=bio if bio is not None else user_info.bio,
			social_link=social_link if social_link is not None else user_info.social_link,
			created_at=user_info.created_at, updated_at=user_info.updated_at
		)

		update = await self.students_table.update_student_info(username, password, student_model)

		if update:
			return student_model



