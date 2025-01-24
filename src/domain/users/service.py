from fastapi import Response, HTTPException, status, Depends, Request

from src.configs.logger_setup import logger
from src.domain.authentication.dependencies import check_user_role
from src.domain.enums import UserRole
from src.domain.users.schema import UsersResponseForPost, UsersModelForPost, UsersModel, AuthorizedUser
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.infrastructure.database.postgres.users.client import UsersTable
from src.domain.authentication.auth import create_access_token, get_token


class UsersRouterService:

	def __init__(self) -> None:
		self.users_table = UsersTable()
		self.students_table = StudentsTable()


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


	# async def add_user_superadmin_service(self, username: str, password: str) -> UsersResponseForPost:
	# 	user_model = UsersModelForPost(
	# 		username=username, password=password, role=UserRole.superadmin
	# 	)
	#
	# 	user_id = await self.users_table.insert_user(user_model)
	# 	await self.students_table.insert_student(username, password)
	#
	# 	return UsersResponseForPost(UserId=user_id)



	async def add_student_service(self, username: str, password: str,
	                              token: str = Depends(get_token)) -> UsersResponseForPost:
		user_role = await check_user_role(token)

		if user_role != UserRole.superadmin and user_role != UserRole.teacher:
			logger.warning("Not enough rights !")
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights !")

		user_model = UsersModelForPost(
			username=username, password=password, role=UserRole.student
		)

		user_id = await self.users_table.insert_user(user_model)
		await self.students_table.insert_student(username, password)

		return UsersResponseForPost(UserId=user_id)


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
