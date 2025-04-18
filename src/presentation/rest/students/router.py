from fastapi import APIRouter, status, Path

from src.domain.students.service import StudentsRouterService
from src.domain.students.schema import StudentsModel, StudentsModelForPatch

students_router = APIRouter(prefix="/Students", tags=["Students"])

students_service = StudentsRouterService()

@students_router.get("", response_model=list[StudentsModel], status_code=status.HTTP_200_OK)
async def get_all_students() -> list[StudentsModel]:
	return await students_service.get_all_students_service()


@students_router.get("/{username}", response_model=StudentsModel, status_code=status.HTTP_200_OK)
async def get_student_by_username(username: str = Path(..., description="Account username of the Student")) -> StudentsModel:
	return await students_service.get_student_by_username_service(username=username)


@students_router.patch("/change_info", response_model=StudentsModel, status_code=status.HTTP_200_OK)
async def update_student_info(student_model: StudentsModelForPatch) -> StudentsModel:
	return await students_service.update_student_service(student_model)


