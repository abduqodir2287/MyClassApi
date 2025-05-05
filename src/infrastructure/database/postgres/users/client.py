from typing import Optional
from sqlalchemy import select, delete, update, inspect

from src.configs.logger_setup import logger
from src.domain.enums import UserRole
from src.domain.users.schema import AddUserModel, UsersModel
from src.infrastructure.database.postgres.models import Users
from src.infrastructure.database.postgres.database import engine
from src.infrastructure.database.postgres.session_manager import AsyncSessionManager



class UsersTable:

	def __init__(self) -> None:
		self.table = Users()
		self.engine = engine
		self.async_session = AsyncSessionManager()


	async def select_users(self, user_id: Optional[int] = None,
	                       username: Optional[str] = None) -> list[UsersModel] | UsersModel:
		async with self.async_session.get_session() as session:

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


	async def insert_user(self, user_model: AddUserModel) -> int:
		async with self.async_session.get_session_begin() as session:

			insert_into = Users(
				username=user_model.username,
				password=user_model.password,
				role=user_model.role
			)
			session.add(insert_into)

			await session.flush()

			await session.refresh(insert_into)

			return insert_into.id


	async def create_user_superadmin(self) -> None:
		async with self.async_session.get_session_begin() as session:

			stmt = await session.execute(select(Users))
			user = stmt.scalars().first()

			if user:
				return

			insert_into = Users(
				username="admin",
				password="password",
				role=UserRole.superadmin,
			)
			session.add(insert_into)

			await session.commit()

			logger.info("First user superadmin created successfully !")


	async def delete_user_by_username(self, username: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
			delete_user = delete(Users).where(username == Users.username)
			result = await session.execute(delete_user)

			await session.commit()

			if result.rowcount > 0:
				return True


	async def update_user_username(self, username: str, password: str, new_username: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
			update_user = update(Users).where(
				username == Users.username, password == Users.password).values(
				username=new_username
			)

			result = await session.execute(update_user)
			await session.commit()

			if result.rowcount > 0:
				return True


	async def update_user_password(self, username: str, password: str, new_password: str) -> bool | None:
		async with self.async_session.get_session_begin() as session:
				update_user = update(Users).where(
					username == Users.username, password == Users.password).values(
					password=new_password
				)

				result = await session.execute(update_user)
				await session.commit()

				if result.rowcount > 0:
					return True


	async def table_exists(self, table_name: str) -> bool:
		async with self.engine.connect() as conn:
			return await conn.run_sync(
				lambda sync_conn: table_name in inspect(sync_conn).get_table_names()
			)


