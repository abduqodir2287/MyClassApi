
from src.domain.students.schema import StudentsModel
from src.infrastructure.database.postgres.students.client import StudentsTable

class StudentsRouterService:

	def __init__(self) -> None:
		self.students_table = StudentsTable()


	async def get_all_students_service(self) -> list[StudentsModel]:
		students_list = []

		for student in await self.students_table.select_all_students():

			returned_student = StudentsModel(
				id=student.id, firstname=student.firstname, lastname=student.lastname,
				photo_url=student.photo_url, birthDate=student.birthDate, age=student.age,
				gender=student.gender, subject=student.subject, interests=student.interests,
				idol=student.idol, created_at=student.created_at, updated_at=student.updated_at
			)

			students_list.append(returned_student)

		return students_list
