from typing import Optional

from src.domain.functions import ClassApiValidationFunctions
from src.domain.students.schema import StudentsModel, StudentsModelForPatch
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.domain.schema import Date


class StudentsRouterService(ClassApiValidationFunctions):

	def __init__(self) -> None:
		self.students_table = StudentsTable()


	async def get_all_students_service(self, search_value: Optional[str] = None, class_id: Optional[int] = None
									   ) -> list[StudentsModel]:

		if class_id is not None:
			students = await self.students_table.select_students(class_id=class_id)
		else:
			students = await self.students_table.select_students_like(search_value=search_value)

		return [
			StudentsModel.model_validate({
				**student.__dict__,
				"birthDate": Date(date=student.birthDate) if student.birthDate else None # type: ignore
			})
			for student in students
		]


	async def get_student_by_username_service(self, username: str) -> StudentsModel:
		get_student = await self.students_table.select_students(username=username)

		await self.check_resource(get_student, detail="Student with this username not found")

		return StudentsModel.model_validate({
			**get_student.__dict__,
			"birthDate": Date(date=get_student.birthDate) if get_student.birthDate else None  # type: ignore
		})



	async def update_student_service(self, student_model: StudentsModelForPatch) -> StudentsModel | None:
		user_info = await self.students_table.select_students(username=student_model.username)

		await self.check_resource(user_info, detail="Student with this username not found")

		await self.check_password(student_model.password, user_info.password)

		if student_model.birthDate is None:
			student_model.birthDate = (
				Date(date=user_info.birthDate) if user_info.birthDate else None  # type: ignore
			)

		student = StudentsModel(
			username=user_info.username, class_id=user_info.class_id, created_at=user_info.created_at,
			firstname=student_model.firstname if student_model.firstname is not None else user_info.firstname,
			lastname=student_model.lastname if student_model.lastname is not None else user_info.lastname,
			birthDate=student_model.birthDate, age=student_model.age if student_model.age is not None else user_info.age,
			gender=student_model.gender if student_model.gender is not None else user_info.gender,
			subject=student_model.subject if student_model.subject is not None else user_info.subject,
			interests=student_model.interests if student_model.interests is not None else user_info.interests,
			idol=student_model.idol if student_model.idol is not None else user_info.idol,
			bio=student_model.bio if student_model.bio is not None else user_info.bio, updated_at=user_info.updated_at,
			social_link=student_model.social_link if student_model.social_link is not None else user_info.social_link,
		)

		update = await self.students_table.update_student_info(student_model.username, student_model.password, student)

		if update:
			return student



