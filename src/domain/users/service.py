from fastapi import Response, HTTPException, status, Depends, Request
from sqlalchemy.exc import IntegrityError

from src.configs.logger_setup import logger
from src.infrastructure.authentication.dependencies import check_user_role
from src.domain.enums import UserRole
from src.domain.users.schema import AddUserModel, AuthorizedUser, UsersModelForPost, UsersModelForPatch, \
	UsersStudentModel, UsersModelForGet, UsersModel
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.infrastructure.database.postgres.teachers.client import TeachersTable
from src.infrastructure.database.postgres.users.client import UsersTable
from src.infrastructure.authentication.service import create_access_token, get_token, decode_access_token
from src.domain.schema import ResponseForPost


class UsersRouterService:

	def __init__(self) -> None:
		self.users_table = UsersTable()
		self.students_table = StudentsTable()
		self.teachers_table = TeachersTable()


	async def get_all_users_service(self) -> list[UsersModelForGet]:
		all_users = []

		for user in await self.users_table.select_users():
			returned_user = UsersModelForGet(
				id=user.id,
				username=user.username,
				role=user.role,
				created_at=user.created_at,
				updated_at=user.updated_at
			)

			all_users.append(returned_user)

		return all_users



	async def get_info_about_user(self, token: str = Depends(get_token)) -> UsersModelForGet:
		user_info = decode_access_token(token)

		info = await self.users_table.select_users(user_id=int(user_info.get("sub")))

		return UsersModelForGet(
			id=info.id, username=info.username, role=info.role,
			created_at=info.created_at, updated_at=info.updated_at
		)



	async def get_user_by_username_service(self, username: str) -> UsersModelForGet:
		user_by_id = await self.users_table.select_users(username=username)

		if not user_by_id:
			logger.warning("User not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username '{username}' not found")

		return 	UsersModelForGet(
			id=user_by_id.id, username=user_by_id.username, role=user_by_id.role,
			created_at=user_by_id.created_at, updated_at=user_by_id.updated_at
		)



	async def get_student_with_password_service(self, username: str, token: str = Depends(get_token)) -> UsersModel:
		user_role = await check_user_role(token)

		if user_role != UserRole.teacher and user_role != UserRole.superadmin:
			logger.warning("Not enough rights!")

			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

		student = await self.users_table.select_users(username=username)

		if not student:
			logger.warning("Student not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student with this username not found")

		return UsersModel(
			id=student.id, username=student.username, password=student.password, role=student.role,
			created_at=student.created_at, updated_at=student.updated_at
		)



	async def user_authorization_service(self, response: Response, user_model: UsersModelForPost) -> AuthorizedUser:
		user_by_username = await self.users_table.select_users(username=user_model.username)

		if user_by_username is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

		if user_by_username.password != user_model.password:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

		access_token = create_access_token({"sub": str(user_by_username.id)})
		response.set_cookie("user_access_token", access_token, httponly=True)

		logger.info("User is successfully authorized")

		return AuthorizedUser(Result="User authorized successfully !")



	async def add_teacher_service(self, user_model: UsersModelForPost,
								  token: str = Depends(get_token)) -> ResponseForPost:
		try:
			user_role = await check_user_role(token)
			allowed_roles = {UserRole.superadmin, UserRole.teacher}

			if user_role not in allowed_roles:
				logger.warning("Not enough rights!")

				raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

			user_id = await self.users_table.insert_user(AddUserModel(
				username=user_model.username, password=user_model.password, role=UserRole.teacher))

			await self.teachers_table.insert_teacher(user_model.username, user_model.password)
			logger.info("Teacher successfully added to DB")

			return ResponseForPost(ID=user_id)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")



	async def add_student_service(self, user_model: UsersStudentModel,
								  token: str = Depends(get_token)) -> ResponseForPost:
		try:
			user_role = await check_user_role(token)

			if user_role != UserRole.superadmin and user_role != UserRole.teacher:
				logger.warning("Not enough rights!")

				raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

			await self.students_table.insert_student(username=user_model.username, password=user_model.password,
													 class_id=user_model.class_id)

			user_id = await self.users_table.insert_user(AddUserModel(
				username=user_model.username, password=user_model.password, role=UserRole.student))

			logger.info("Teacher successfully added to DB")

			return ResponseForPost(ID=user_id)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
								detail="Incorrect Class ID or User with this username already exists")



	async def add_just_user_service(self, response: Response, user_model: UsersModelForPost) -> AuthorizedUser:
		try:
			user_model = AddUserModel(username=user_model.username, password=user_model.password, role=UserRole.user)

			user_id = await self.users_table.insert_user(user_model)

			access_token = create_access_token({"sub": str(user_id)})
			response.set_cookie("user_access_token", access_token, httponly=True)

			logger.info("User authorized successfully!")

			return AuthorizedUser(Result="User authorized successfully!")

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
								detail="User with this username already exists")



	async def update_user_service(self, user_model: UsersModelForPatch) -> None:
		try:
			get_user = await self.users_table.select_users(username=user_model.username)

			if get_user is None:
				logger.warning("User not found")
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

			if get_user.password != user_model.password:
				logger.warning("The user entered an incorrect password.")
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

			await self.users_table.update_user_username(user_model.username, user_model.password, user_model.new_username)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")



	async def delete_user_service(self, username: str, token: str = Depends(get_token)) -> None:
		user_role = await check_user_role(token)

		user_info = await self.users_table.select_users(username=username)

		if user_role != UserRole.superadmin and user_role != UserRole.teacher:
			logger.warning("Not enough rights !")
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights !")

		delete_user = await self.users_table.delete_user_by_username(username)

		if delete_user is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this username not found")

		if user_info.role == UserRole.student:
			await self.students_table.delete_student_by_username(username=username)

		elif user_info.role == UserRole.teacher:
			await self.teachers_table.delete_teacher_by_username(username=username)


		logger.info("User deleted successfully")



	@staticmethod
	async def logout_service(request: Request, response: Response) -> None:
		access_token = request.cookies.get("user_access_token")

		if not access_token:
			logger.warning("Token not found")
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized")

		response.delete_cookie(key="user_access_token")

		logger.info("User logged out successfully")
