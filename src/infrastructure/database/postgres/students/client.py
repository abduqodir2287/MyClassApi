from sqlalchemy import select, delete

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


	async def select_all_students(self) -> list[StudentsModel]:
		async with self.async_session() as session:
			select_students = select(Students)

			all_students = await session.execute(select_students)

			return all_students.scalars().all()



