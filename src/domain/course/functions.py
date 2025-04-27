from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional

from src.configs.logger_setup import logger
from src.domain.course.schema import ClassModel
from src.infrastructure.database.postgres.students.client import StudentsTable


class ClassRouterFunctions:

    def __init__(self, students_table: StudentsTable) -> None:
        self.students_table = students_table


    @staticmethod
    async def class_model_formatter(
            class_id: int, class_name: str, teacher_username: str, students_count: int,
            school_year: str, class_leader_username: Optional[str] = None, description: Optional[str] = None,
            class_room_number: Optional[int] = None, created_at: datetime = ..., updated_at: datetime = ...
    ) -> ClassModel:

        return ClassModel(
            id=class_id, class_name=class_name, teacher_username=teacher_username, students_count=students_count,
            school_year=school_year, class_leader_username=class_leader_username, description=description,
            class_room_number=class_room_number, created_at=created_at, updated_at=updated_at
        )



    async def check_class_leader(self, class_id: int, class_leader_username: Optional[str] = None) -> None:
        if class_leader_username:
            class_leader_info = await self.students_table.select_students(username=class_leader_username)

            if not class_leader_info:
                logger.warning("Class leader not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="A student with this username does not exist"
                )

            if class_leader_info.class_id != class_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="A student with this username is not in this class"
                )


