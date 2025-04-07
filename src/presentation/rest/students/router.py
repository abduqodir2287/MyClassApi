from fastapi import APIRouter, status, Query, Path
from typing import Optional

from src.domain.schema import Date
from src.domain.students.service import StudentsRouterService
from src.domain.enums import Gender
from src.domain.students.schema import StudentsModel

students_router = APIRouter(prefix="/Students", tags=["Students"])

students_service = StudentsRouterService()

@students_router.get("", response_model=list[StudentsModel], status_code=status.HTTP_200_OK)
async def get_all_students() -> list[StudentsModel]:
	return await students_service.get_all_students_service()


@students_router.get("/{username}", response_model=StudentsModel, status_code=status.HTTP_200_OK)
async def get_student_by_username(username: str = Path(..., description="Account username of the Student")) -> StudentsModel:
	return await students_service.get_student_by_username_service(username=username)


@students_router.patch("/change_info/{username}", response_model=StudentsModel, status_code=status.HTTP_200_OK)
async def update_student_info(
		username: str = Path(..., description="Username of the Student"),
		password: str = Query(..., description="Password of the User"), firstname: Optional[str] = None,
		lastname: Optional[str] = None, birth_date: Optional[Date] = None, age: Optional[int] = None,
		gender: Optional[Gender] = None, subject: Optional[str] = None, interests: Optional[str] = None,
		idol: Optional[str] = None, bio: Optional[str] = None, social_link: Optional[str] = None
) -> StudentsModel:
	return await students_service.update_student_service(username, password, firstname, lastname, birth_date, age,
														 gender, subject, interests, idol, bio, social_link)


