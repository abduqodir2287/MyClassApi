from fastapi import APIRouter, status, Query, Depends

from src.infrastructure.authentication.service import get_token
from src.domain.course.schema import ClassModel
from src.domain.course.service import ClassRouterService
from src.domain.schema import ResponseForPost

class_router = APIRouter(prefix="/Class", tags=["Class"])

class_service = ClassRouterService()


@class_router.get("", response_model=list[ClassModel], status_code=status.HTTP_200_OK)
async def get_all_classes() -> list[ClassModel]:
    return await class_service.get_all_classes_service()


@class_router.post("", response_model=ResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_class(
        class_name: str = Query(..., description="Name of the class", example="11-b, 5-a"),
        students_count: int = Query(..., description="Number of students in a class"),
        teacher_id: int = Query(..., description="The Class Teacher ID"),
        school_year: str = Query(..., description="Academic year", example="2024-2025"), token: str = Depends(get_token)
) -> ResponseForPost:
    return await class_service.add_class_service(class_name, students_count, teacher_id, school_year, token)



