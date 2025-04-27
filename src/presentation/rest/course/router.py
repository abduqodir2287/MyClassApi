from typing import Optional
from fastapi import APIRouter, status, Query, Depends, Path

from src.infrastructure.authentication.service import get_token
from src.domain.course.schema import ClassModel, GetFullClassInfo
from src.domain.course.service import ClassRouterService
from src.domain.schema import ResponseForPost

class_router = APIRouter(prefix="/Class", tags=["Class"])

class_service = ClassRouterService()


@class_router.get("", response_model=list[ClassModel], status_code=status.HTTP_200_OK)
async def get_all_classes(class_name: Optional[str] = Query(
    None, description="The name of the class you want to get")) -> list[ClassModel]:
    return await class_service.get_all_classes_service(class_name=class_name)



@class_router.get("/{class_name}", response_model=GetFullClassInfo, status_code=status.HTTP_200_OK)
async def get_full_class_info(class_name: str = Path(
    ..., description="The name of the class you want to get")) -> GetFullClassInfo:
    return await class_service.get_full_class_info_service(class_name)


@class_router.post("", response_model=ResponseForPost, status_code=status.HTTP_201_CREATED)
async def add_class(
        class_name: str = Query(..., description="Name of the class", example="11-B, 5-A"),
        students_count: int = Query(..., description="Number of students in a class"),
        teacher_username: str = Query(..., description="The Class Teacher username"),
        school_year: str = Query(..., description="Academic year", example="2024-2025"), token: str = Depends(get_token)
) -> ResponseForPost:
    return await class_service.add_class_service(class_name, students_count, teacher_username, school_year, token)


@class_router.patch("/change_info", response_model=ClassModel, status_code=status.HTTP_200_OK)
async def update_class_info(
        class_name: str = Query(..., description="The name of the class you want to change (for example, 11-b, 5-a)"),
        students_count: Optional[int] = Query(None, description="Number of students in a class"),
        school_year: Optional[str] = Query(None, description="Academic year"),
        class_leader_username: Optional[str] = Query(None, description="Unique class leader ID"),
        description: Optional[str] = Query(None, description="Description for Class"),
        class_room_number: Optional[int] = Query(None, description="Just Class room number"),
        token: str = Depends(get_token)
) -> ClassModel:
    return await class_service.update_class_info_service(class_name, students_count, school_year, class_leader_username,
                                                         description, class_room_number, token)


