from fastapi import HTTPException, status

from src.domain.enums import UserRole
from src.domain.users.schema import UsersResponseForPost, UsersModelForPost, UsersModel
from src.infrastructure.database.postgres.users.client import UsersTable


class UsersRouterService:

	def __init__(self) -> None:
		self.table = UsersTable()


	async def add_user_service(self, username: str, password: str, role: UserRole) -> UsersResponseForPost:
		user_model = UsersModelForPost(
			username=username, password=password, role=role
		)

		user_id = await self.table.insert_user(user_model)

		return UsersResponseForPost(UserId=user_id)


	async def get_all_users(self) -> list[UsersModel]:
		all_users = []

		for user in await self.table.select_all_users():
			returned_user = UsersModel(
				id=user.id,
				username=user.username,
				password=user.password,
				role=user.role,
				created_at=user.created_at,
				updated_at=user.updated_at
			)

			all_users.append(returned_user)

		return all_users

