from fastapi import APIRouter, status, Query

from src.domain.enums import UserRole
from src.domain.users.schema import UsersResponseForPost, UsersModel
from src.domain.users.service import UsersRouterService

users_router = APIRouter(prefix="/Users", tags=["Users"])

users_service = UsersRouterService()


@users_router.get("", response_model=list[UsersModel], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[UsersModel]:
	return await users_service.get_all_users()


@users_router.post("", response_model=UsersResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_user(
		username: str = Query(..., description="Username of the user (e.g., Unique)", min_length=3, max_length=50),
		password: str = Query(..., description="User's Password", min_length=8, max_length=50),
		role: UserRole = Query(..., description="Role assigned to the user (e.g., superadmin or user)")
) -> UsersResponseForPost:
	return await users_service.add_user_service(username, password, role)


