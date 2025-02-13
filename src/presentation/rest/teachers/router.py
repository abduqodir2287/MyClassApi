from fastapi import APIRouter, status, Query, Response, Depends, Request, Path

from src.domain.authentication.auth import get_token
from src.domain.enums import UserRole
from src.domain.teachers.schema import TeachersModel
from src.domain.teachers.service import TeachersRouterService

teachers_router = APIRouter(prefix="/Teachers", tags=["Teacher"])

teachers_service = TeachersRouterService()


@teachers_router.get("", response_model=list[TeachersModel], status_code=status.HTTP_200_OK)
async def get_all_teachers() -> list[TeachersModel]:
	return await teachers_service.get_all_teachers()

