from typing import Optional
from fastapi import APIRouter, status, Path

from src.domain.teachers.schema import TeachersModel, TeachersModelForPatch
from src.domain.teachers.service import TeachersRouterService

teachers_router = APIRouter(prefix="/Teachers", tags=["Teacher"])

teachers_service = TeachersRouterService()


@teachers_router.get("", response_model=list[TeachersModel], status_code=status.HTTP_200_OK)
async def get_all_teachers(search_value: Optional[str] = None) -> list[TeachersModel]:
	return await teachers_service.get_all_teachers_service(search_value)


@teachers_router.get("/{username}", response_model=TeachersModel, status_code=status.HTTP_200_OK)
async def get_by_username(
		username: str = Path(..., description="Account username of the Teacher")
) -> TeachersModel:
	return await teachers_service.get_teacher_by_username_service(username=username)


@teachers_router.patch("/change_info", response_model=TeachersModel, status_code=status.HTTP_200_OK)
async def update_teacher_info(teacher_model: TeachersModelForPatch) -> TeachersModel:
	return await teachers_service.update_teacher_info_service(teacher_model)


