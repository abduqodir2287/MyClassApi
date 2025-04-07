from fastapi import Response, HTTPException, status, Depends, Request
from sqlalchemy.exc import IntegrityError

from src.configs.logger_setup import logger
from src.domain.authentication.dependencies import check_user_role
from src.domain.enums import UserRole
from src.domain.users.schema import UsersResponseForPost, UsersModelForPost, UsersModel, AuthorizedUser
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.infrastructure.database.postgres.teachers.client import TeachersTable
from src.infrastructure.database.postgres.users.client import UsersTable
from src.domain.authentication.auth import create_access_token, get_token, decode_access_token


class UsersRouterService:

	def __init__(self) -> None:
		self.users_table = UsersTable()
		self.students_table = StudentsTable()
		self.teachers_table = TeachersTable()


	async def get_all_users(self) -> list[UsersModel]:
		all_users = []

		for user in await self.users_table.select_users():
			returned_user = UsersModel(
				id=user.id,
				username=user.username,
				role=user.role,
				created_at=user.created_at,
				updated_at=user.updated_at
			)

			all_users.append(returned_user)

		return all_users


	async def get_info_about_user(self, token: str = Depends(get_token)) -> UsersModel:
		user_info = decode_access_token(token)

		info = await self.users_table.select_users(user_id=int(user_info.get("sub")))

		return UsersModel(
			id=info.id, username=info.username, role=info.role,
			created_at=info.created_at, updated_at=info.updated_at
		)


	async def user_authorization_service(self, response: Response, username: str, password: str) -> AuthorizedUser:
		user_by_username = await self.users_table.select_users(username=username)

		if user_by_username is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

		if user_by_username.password != password:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

		access_token = create_access_token({"sub": str(user_by_username.id)})
		response.set_cookie("user_access_token", access_token, httponly=True)

		logger.info("User is successfully authorized")

		return AuthorizedUser(Result="User authorized successfully !")


	async def add_user_service(self, username: str, password: str, role: UserRole,
							   token: str = Depends(get_token)) -> UsersResponseForPost:
		try:
			user_role = await check_user_role(token)
			allowed_roles = {UserRole.superadmin, UserRole.teacher}

			if user_role not in allowed_roles or (role == UserRole.superadmin and user_role != UserRole.superadmin):
				logger.warning("Not enough rights!")
				raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

			user_id = await self.users_table.insert_user(UsersModelForPost(username=username, password=password, role=role))

			if role == UserRole.student:
				await self.students_table.insert_student(username, password)

				logger.info("Student successfully added to DB")

			if role == UserRole.teacher:
				await self.teachers_table.insert_teacher(username, password)

				logger.info("Teacher successfully added to DB")

			return UsersResponseForPost(UserId=user_id)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")


	async def update_user_service(self, username: str, password: str, new_username: str) -> None:
		try:
			get_user = await self.users_table.select_users(username=username)

			if get_user is None:
				logger.warning("User not found")
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

			if get_user.password != password:
				logger.warning("The user entered an incorrect password.")
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

			await self.users_table.update_user_username(username, password, new_username)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")



	async def delete_user_service(self, username: str, token: str = Depends(get_token)) -> None:
		user_role = await check_user_role(token)

		if user_role != UserRole.superadmin and user_role != UserRole.teacher:
			logger.warning("Not enough rights !")
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights !")

		delete_user = await self.users_table.delete_user_by_username(username)
		print(delete_user)

		if delete_user is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

		logger.info("User deleted successfully")


	@staticmethod
	async def logout_service(request: Request, response: Response) -> None:
		access_token = request.cookies.get("user_access_token")

		if not access_token:
			logger.warning("Token not found")
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized")

		response.delete_cookie(key="user_access_token")

		logger.info("User logged out successfully")
