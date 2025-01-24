from fastapi import APIRouter, status, Query, Response, Depends, Request, Path

from src.domain.authentication.auth import get_token
from src.domain.users.schema import UsersResponseForPost, UsersModel, AuthorizedUser
from src.domain.users.service import UsersRouterService

users_router = APIRouter(prefix="/Users", tags=["Users"])

users_service = UsersRouterService()


@users_router.get("", response_model=list[UsersModel], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[UsersModel]:
	return await users_service.get_all_users()


@users_router.post("/authorization", response_model=AuthorizedUser, status_code=status.HTTP_200_OK)
async def user_authorization(
		response: Response,
		username: str = Query(..., description="Username of the user", min_length=3, max_length=50),
		password: str = Query(..., description="User's Password", min_length=8, max_length=50)
) -> AuthorizedUser:
	return await users_service.user_authorization_service(response, username, password)


@users_router.post("/Student", response_model=UsersResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_student(
		token: str = Depends(get_token),
		username: str = Query(..., description="Username of the user (e.g., Unique)", min_length=3, max_length=50),
		password: str = Query(..., description="User's Password", min_length=8, max_length=50)
) -> UsersResponseForPost:
	return await users_service.add_student_service(username, password, token)


@users_router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(
		token: str = Depends(get_token), username: str = Path(..., description="The username you want to delete")
) -> None:
	await users_service.delete_user_service(username, token)


@users_router.post("/logout_user", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response, request: Request) -> None:
	await users_service.logout_service(request, response)


