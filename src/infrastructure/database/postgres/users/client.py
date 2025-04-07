from typing import Optional
from sqlalchemy import select, delete, update

from src.domain.users.schema import UsersModelForPost, UsersModel
from src.infrastructure.database.postgres.models import Users
from src.infrastructure.database.postgres.database import Base

class UsersTable:

	def __init__(self) -> None:
		self.table = Users()
		self.async_session = Base.async_session


	async def select_users(self, user_id: Optional[int] = None,
	                       username: Optional[str] = None) -> list[UsersModel] | UsersModel:
		async with self.async_session() as session:

			if username is not None:
				select_user = select(Users).where(username == Users.username)

				user = await session.execute(select_user)

				return user.scalars().first()

			elif user_id is not None:
				select_user = select(Users).where(user_id == Users.id)

				user = await session.execute(select_user)

				return user.scalars().first()

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


	async def delete_user_by_username(self, username: str) -> bool | None:
		async with self.async_session() as session:
			async with session.begin():
				delete_user = delete(Users).where(username == Users.username)
				result = await session.execute(delete_user)

				await session.commit()

				if result.rowcount > 0:
					return True


	async def update_user_username(self, username: str, password: str, new_username: str) -> bool | None:
		async with self.async_session() as session:
			async with session.begin():
				update_user = update(Users).where(
					username == Users.username, password == Users.password).values(
					username=new_username
				)

				result = await session.execute(update_user)
				await session.commit()

				if result.rowcount > 0:
					return True


