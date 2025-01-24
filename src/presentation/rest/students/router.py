from fastapi import APIRouter, status, Query

from src.domain.students.schema import StudentsModel
from src.domain.students.service import StudentsRouterService

students_router = APIRouter(prefix="/Students", tags=["Students"])

students_service = StudentsRouterService()

@students_router.get("", response_model=list[StudentsModel], status_code=status.HTTP_200_OK)
async def get_all_students() -> list[StudentsModel]:
	return await students_service.get_all_students_service()


