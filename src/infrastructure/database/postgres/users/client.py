from sqlalchemy import select

from src.domain.users.schema import UsersModelForPost, UsersModel
from src.infrastructure.database.postgres.models import Users
from src.infrastructure.database.postgres.database import Base

class UsersTable:

	def __init__(self) -> None:
		self.table = Users()
		self.async_session = Base.async_session


	async def select_all_users(self) -> list[UsersModel]:
		async with self.async_session() as session:
			select_users = select(Users)

			all_users = await session.execute(select_users)

			return all_users.scalars().all()


	async def insert_user(self, user_model: UsersModelForPost) -> int:
		async with self.async_session() as session:
			async with session.begin():

				insert_into = Users(
					username=user_model.username,
					password=user_model.password,
					role=user_model.role
				)
				session.add(insert_into)

			await session.commit()

			await session.refresh(insert_into)

			return insert_into.id



