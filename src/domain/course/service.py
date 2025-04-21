from typing import Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError

from src.configs.logger_setup import logger
from src.infrastructure.authentication.service import get_token
from src.infrastructure.authentication.dependencies import check_user_role
from src.domain.course.schema import ClassModel, ClassModelForPost
from src.domain.enums import UserRole
from src.domain.schema import ResponseForPost
from src.infrastructure.database.postgres.course.client import ClassTable
from src.infrastructure.database.postgres.students.client import StudentsTable
from src.infrastructure.database.postgres.teachers.client import TeachersTable
from src.infrastructure.database.postgres.users.client import UsersTable


class ClassRouterService:

    def __init__(self) -> None:
        self.class_table = ClassTable()
        self.users_table = UsersTable()
        self.students_table = StudentsTable()
        self.teachers_table = TeachersTable()


    async def get_all_classes_service(self) -> list[ClassModel]:
        all_classes = []

        for course in await self.class_table.select_classes():
            returned_class = ClassModel(
                id=course.id,
                class_name=course.class_name,
                students_count=course.students_count,
                teacher_username=course.teacher_username,
                school_year=course.school_year,
                class_leader_username=course.class_leader_username,
                description=course.description,
                class_room_number=course.class_room_number,
                created_at=course.created_at,
                updated_at=course.updated_at
            )

            all_classes.append(returned_class)

        return all_classes



    async def add_class_service(self, class_name: str, students_count: int, teacher_username: str, school_year: str,
                                token: str = Depends(get_token)) -> ResponseForPost:
        try:
            user_role = await check_user_role(token)
            allowed_roles = {UserRole.superadmin, UserRole.teacher}

            if user_role not in allowed_roles:
                logger.warning("Not enough rights!")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

            class_model = ClassModelForPost(class_name=class_name, students_count=students_count,
                                            teacher_username=teacher_username, school_year=school_year)

            class_id = await self.class_table.insert_class(class_model=class_model)

            if class_id:
                return ResponseForPost(ID=class_id)

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Teacher with this username not found!")



    async def update_class_info_service(
            self, class_name: str, students_count: Optional[int] = None, school_year: Optional[str] = None,
            class_leader_username: Optional[str] = None, description: Optional[str] = None,
            class_room_number: Optional[int] = None, token: str = Depends(get_token)
    ) -> ClassModel | None:
        user_role = await check_user_role(token)

        if user_role != UserRole.teacher and user_role != UserRole.superadmin:

            logger.warning("Not enough rights!")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

        class_info = await self.class_table.select_classes(class_name=class_name)

        if not class_info:
            logger.info("Class not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class with this class name not found")

        if all(value is None for value in
               [students_count, school_year, class_leader_username, description, class_room_number]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update."
            )

        if class_leader_username is not None:
            class_leader_info = await self.students_table.select_students(username=class_leader_username)

            if not class_leader_info:
                logger.warning("Class leader not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A student with this username does not exist "
                                                                                  "or is not in this class")

            if class_leader_info.class_id != class_info.id:
                logger.warning("This student does not study in this class")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This student does not study in this class")

        class_model = ClassModel(
            id=class_info.id, class_name=class_name, teacher_username=class_info.teacher_username,
            students_count=students_count if students_count is not None else class_info.students_count,
            school_year=school_year if school_year is not None else class_info.school_year,
            class_leader_username=class_leader_username if class_leader_username is not None else class_info.class_leader_username,
            description=description if description is not None else class_info.description,
            class_room_number=class_room_number if class_room_number is not None else class_info.class_room_number,
            created_at=class_info.created_at, updated_at=class_info.updated_at
        )

        update = await self.class_table.update_class_info(class_model)

        if update:
            return class_model



