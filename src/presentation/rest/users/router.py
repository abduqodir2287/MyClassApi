from fastapi import APIRouter, status, Response, Depends, Request, Path, Body

from src.infrastructure.authentication.service import get_token
from src.domain.schema import ResponseForPost
from src.domain.users.schema import AuthorizedUser, UsersModelForPost, UsersModelForPatch, \
	UsersStudentModel, UsersModelForGet, UsersModel, ChangePasswordModel
from src.domain.users.service import UsersRouterService

users_router = APIRouter(prefix="/Users", tags=["Users"])

users_service = UsersRouterService()


@users_router.get("", response_model=list[UsersModelForGet], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[UsersModelForGet]:
	return await users_service.get_all_users_service()


@users_router.post("/authorization", response_model=AuthorizedUser, status_code=status.HTTP_200_OK)
async def user_authorization(
		response: Response, user_model: UsersModelForPost = Body(...)
) -> AuthorizedUser:
	return await users_service.user_authorization_service(response, user_model)


@users_router.post("/add_user", response_model=AuthorizedUser, status_code=status.HTTP_201_CREATED)
async def add_just_user(
		response: Response, user_model: UsersModelForPost = Body(...)
) -> AuthorizedUser:
	return await users_service.add_just_user_service(response, user_model)


@users_router.get("/user_info", response_model=UsersModelForGet, status_code=status.HTTP_200_OK)
async def user_info(token: str = Depends(get_token)) -> UsersModelForGet:
	return await users_service.get_info_about_user(token)


@users_router.get("/{username}", response_model=UsersModelForGet, status_code=status.HTTP_200_OK)
async def get_user_by_username(
		username: str = Path(..., description="User's username")
) -> UsersModelForGet:
	return await users_service.get_user_by_username_service(username)


@users_router.get("/get_student/with_password/{username}", response_model=UsersModel, status_code=status.HTTP_200_OK)
async def get_student_with_password(
		username: str = Path(..., description="Student's username"), token: str = Depends(get_token)
) -> UsersModel:
	return await users_service.get_student_with_password_service(username, token)


@users_router.post("/add_teacher", response_model=ResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_teacher_user(
		token: str = Depends(get_token), user_model: UsersModelForPost = Body(...)
) -> ResponseForPost:
	return await users_service.add_teacher_service(user_model, token)


@users_router.post("/add_student", response_model=ResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_student_user(
		token: str = Depends(get_token), user_model: UsersStudentModel = Body(...)
) -> ResponseForPost:
	return await users_service.add_student_service(user_model, token)


@users_router.patch("/change_username", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_username(
		users_model: UsersModelForPatch = Body(...)
) -> None:
	await users_service.update_user_service(users_model)


@users_router.patch("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
		users_model: ChangePasswordModel = Body(...)
) -> None:
	await users_service.update_user_password_service(users_model)


@users_router.delete("/delete_user/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(
		token: str = Depends(get_token),
		username: str = Path(..., description="The username you want to delete")
) -> None:
	await users_service.delete_user_service(username, token)


@users_router.post("/logout_user", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response, request: Request) -> None:
	await users_service.logout_service(request, response)


