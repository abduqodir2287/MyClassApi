from fastapi import HTTPException, status

from src.configs.logger_setup import logger
from src.domain.students.schema import StudentsModel, StudentsModelForPatch
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.domain.schema import Date

class StudentsRouterService:

	def __init__(self) -> None:
		self.students_table = StudentsTable()


	async def get_all_students_service(self) -> list[StudentsModel]:
		students_list = []

		for student in await self.students_table.select_students():

			returned_student = StudentsModel(id=student.id, username=student.username,
				class_id=student.class_id, firstname=student.firstname, lastname=student.lastname,
				birthDate=Date(date=student.birthDate) if student.birthDate is not None else student.birthDate, # type: ignore
				age=student.age, gender=student.gender, subject=student.subject, interests=student.interests,
				idol=student.idol, bio=student.bio, social_link=student.social_link,
				created_at=student.created_at, updated_at=student.updated_at
			)

			students_list.append(returned_student)

		return students_list



	async def get_student_by_username_service(self, username: str) -> StudentsModel:
		get_student = await self.students_table.select_students(username=username)

		if not get_student:
			logger.warning("Student not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with this username not found")

		return StudentsModel(
				id=get_student.id, username=get_student.username, firstname=get_student.firstname,
				class_id=get_student.class_id, lastname=get_student.lastname,
				birthDate=Date(date=get_student.birthDate) if get_student.birthDate is not None else get_student.birthDate, # type: ignore
				age=get_student.age, gender=get_student.gender, subject=get_student.subject, interests=get_student.interests,
				idol=get_student.idol, bio=get_student.bio, social_link=get_student.social_link,
				created_at=get_student.created_at, updated_at=get_student.updated_at
			)



	async def update_student_service(self, student_model: StudentsModelForPatch) -> StudentsModel | None:
		user_info = await self.students_table.select_students(username=student_model.username)

		if not user_info:
			logger.warning("Student not found")
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Student with this username not found"
			)

		if user_info.password != student_model.password:
			logger.warning("Wrong password")
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="You are writing the wrong password."
			)

		if student_model.birthDate is None:
			student_model.birthDate = (
				Date(date=user_info.birthDate) if user_info.birthDate else None  # type: ignore
			)

		student = StudentsModel(
			id=user_info.id, username=user_info.username, class_id=user_info.class_id,
			firstname=student_model.firstname if student_model.firstname is not None else user_info.firstname,
			lastname=student_model.lastname if student_model.lastname is not None else user_info.lastname,
			birthDate=student_model.birthDate, age=student_model.age if student_model.age is not None else user_info.age,
			gender=student_model.gender if student_model.gender is not None else user_info.gender,
			subject=student_model.subject if student_model.subject is not None else user_info.subject,
			interests=student_model.interests if student_model.interests is not None else user_info.interests,
			idol=student_model.idol if student_model.idol is not None else user_info.idol,
			bio=student_model.bio if student_model.bio is not None else user_info.bio,
			social_link=student_model.social_link if student_model.social_link is not None else user_info.social_link,
			created_at=user_info.created_at, updated_at=user_info.updated_at
		)

		update = await self.students_table.update_student_info(student_model.username, student_model.password, student)

		if update:
			return student



