from fastapi import Response, HTTPException, status, Depends, Request
from sqlalchemy.exc import IntegrityError

from src.configs.logger_setup import logger
from src.domain.functions import ClassApiValidationFunctions
from src.domain.enums import UserRole
from src.domain.users.schema import AddUserModel, AuthorizedUser, UsersModelForPost
from src.domain.users.schema import ChangePasswordModel, UsersModelForPatch
from src.domain.users.schema import	UsersStudentModel, UsersModelForGet, UsersModel
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.infrastructure.database.postgres.teachers.client import TeachersTable
from src.infrastructure.database.postgres.users.client import UsersTable
from src.infrastructure.authentication.service import create_access_token, get_token, decode_access_token
from src.domain.schema import ResponseForPost


class UsersRouterService(ClassApiValidationFunctions):

	def __init__(self) -> None:
		self.users_table = UsersTable()
		self.students_table = StudentsTable()
		self.teachers_table = TeachersTable()


	async def get_all_users_service(self) -> list[UsersModelForGet]:
		all_users = await self.users_table.select_users()

		return [UsersModelForGet.model_validate(user) for user in all_users]



	async def get_info_about_user(self, token: str = Depends(get_token)) -> UsersModelForGet:
		user_info = decode_access_token(token)

		info = await self.users_table.select_users(user_id=int(user_info.get("sub")))

		return UsersModelForGet.model_validate(info)



	async def get_user_by_username_service(self, username: str) -> UsersModelForGet:
		user_by_id = await self.users_table.select_users(username=username)

		await self.check_resource(resource=user_by_id, detail=f"User with username '{username}' not found")

		return UsersModelForGet.model_validate(user_by_id)



	async def get_student_with_password_service(
			self, username: str, token: str = Depends(get_token)
	) -> UsersModel:
		await self.check_role_teacher_and_superadmin(token)

		student = await self.users_table.select_users(username=username)

		await self.check_resource(resource=student, detail="Student with this username not found")

		return UsersModel.model_validate(student)



	async def user_authorization_service(
			self, response: Response, user_model: UsersModelForPost
	) -> AuthorizedUser:
		user_by_username = await self.users_table.select_users(username=user_model.username)

		await self.check_resource(resource=user_by_username, detail="User with this username not found")

		await self.check_password(user_model.password, user_by_username.password)

		access_token = create_access_token({"sub": str(user_by_username.id)})
		response.set_cookie("user_access_token", access_token, httponly=True)

		logger.info("User is successfully authorized")

		return AuthorizedUser(Result="User authorized successfully !")



	async def add_teacher_service(
			self, user_model: UsersModelForPost, token: str = Depends(get_token)
	) -> ResponseForPost:
		try:
			await self.check_role_teacher_and_superadmin(token)

			user_id = await self.users_table.insert_user(user_model=AddUserModel(
				username=user_model.username, password=user_model.password, role=UserRole.teacher))

			await self.teachers_table.insert_teacher(user_model.username, user_model.password)
			logger.info("Teacher successfully added to DB")

			return ResponseForPost(ID=user_id)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")



	async def add_student_service(
			self, user_model: UsersStudentModel, token: str = Depends(get_token)
	) -> ResponseForPost:
		try:
			await self.check_role_teacher_and_superadmin(token)

			await self.students_table.insert_student(
				username=user_model.username,
				password=user_model.password, class_id=user_model.class_id
			)

			user_id = await self.users_table.insert_user(user_model=AddUserModel(
				username=user_model.username, password=user_model.password, role=UserRole.student))

			logger.info("Teacher successfully added to DB")

			return ResponseForPost(ID=user_id)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
								detail="Incorrect Class ID or User with this username already exists")



	async def add_just_user_service(
			self, response: Response, user_model: UsersModelForPost
	) -> AuthorizedUser:
		try:
			user_model = AddUserModel(username=user_model.username, password=user_model.password, role=UserRole.user)

			user_id = await self.users_table.insert_user(user_model=user_model)

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

			await self.check_resource(resource=get_user, detail="User with this username not found")
			await self.check_password(user_model.password, get_user.password)

			if get_user.role == UserRole.teacher:
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher username cannot be changed")

			await self.users_table.update_user_username(user_model.username,
														user_model.password, user_model.new_username)

			if get_user.role == UserRole.student:
				await self.students_table.update_student_username(user_model.username,
																  user_model.password, user_model.new_username)

		except IntegrityError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")



	async def update_user_password_service(self, user_model: ChangePasswordModel) -> None:
		get_user = await self.users_table.select_users(username=user_model.username)

		await self.check_resource(resource=get_user, detail="User with this username not found")
		await self.check_password(user_model.password, get_user.password)

		if get_user.role == UserRole.student:
			await self.students_table.update_student_password(user_model.username,
															  user_model.password, user_model.new_password)

		elif get_user.role == UserRole.teacher:
			await self.teachers_table.update_teacher_password(user_model.username,
															  user_model.password, user_model.new_password)

		await self.users_table.update_user_password(user_model.username, user_model.password, user_model.new_password)



	async def delete_user_service(self, username: str, token: str = Depends(get_token)) -> None:
		await self.check_role_teacher_and_superadmin(token)

		user_info = await self.users_table.select_users(username=username)

		await self.check_resource(resource=user_info, detail="User with this username not found")

		if user_info.role == UserRole.superadmin or user_info.role == UserRole.teacher:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Are you crazy? You can't delete a superadmin and teacher.")

		await self.users_table.delete_user_by_username(username)

		if user_info.role == UserRole.student:
			await self.students_table.delete_student_by_username(username)


		logger.info("User deleted successfully")


	async def add_first_user(self) -> None:
		exist_table = await self.users_table.table_exists("users")

		if not exist_table:
			logger.info("Table Users not found")
			return

		await self.users_table.create_user_superadmin()



	@staticmethod
	async def logout_service(request: Request, response: Response) -> None:
		access_token = request.cookies.get("user_access_token")

		if not access_token:
			logger.warning("Token not found")
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized")

		response.delete_cookie(key="user_access_token")

		logger.info("User logged out successfully")

