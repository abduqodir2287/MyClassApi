from typing import Optional
from fastapi import APIRouter, status, Query, Path

from src.domain.schema import Date
from src.domain.teachers.schema import TeachersModel
from src.domain.teachers.service import TeachersRouterService

teachers_router = APIRouter(prefix="/Teachers", tags=["Teacher"])

teachers_service = TeachersRouterService()


@teachers_router.get("", response_model=list[TeachersModel], status_code=status.HTTP_200_OK)
async def get_all_teachers() -> list[TeachersModel]:
	return await teachers_service.get_all_teachers_service()


@teachers_router.get("/{username}", response_model=TeachersModel, status_code=status.HTTP_200_OK)
async def get_all_teachers(username: str = Path(..., description="Account username of the Teacher")) -> TeachersModel:
	return await teachers_service.get_teacher_by_username_service(username=username)


@teachers_router.patch("/change_info/{username}", response_model=TeachersModel, status_code=status.HTTP_200_OK)
async def update_teacher_info(
		username: str = Path(..., description="Username of the Student"),
		password: str = Query(..., description="Password of the User"), firstname: Optional[str] = None,
		lastname: Optional[str] = None, birth_date: Optional[Date] = None, age: Optional[int] = None,
		subject: Optional[str] = None, idol: Optional[str] = None, bio: Optional[str] = None,
		social_link: Optional[str] = None
) -> TeachersModel:
	return await teachers_service.update_teacher_info_service(username, password, firstname, lastname, birth_date,
															  age, subject, idol, bio, social_link)


