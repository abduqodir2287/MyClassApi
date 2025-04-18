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
                teacher_id=course.teacher_id,
                school_year=course.school_year,
                class_leader_id=course.class_leader_id,
                description=course.description,
                class_room_number=course.class_room_number,
                created_at=course.created_at,
                updated_at=course.updated_at
            )

            all_classes.append(returned_class)

        return all_classes



    async def add_class_service(self, class_name: str, students_count: int, teacher_id: int, school_year: str,
                               token: str = Depends(get_token)) -> ResponseForPost:
        try:
            user_role = await check_user_role(token)
            allowed_roles = {UserRole.superadmin, UserRole.teacher}

            if user_role not in allowed_roles:
                logger.warning("Not enough rights!")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights!")

            class_model = ClassModelForPost(class_name=class_name, students_count=students_count,
                                            teacher_id=teacher_id, school_year=school_year)

            class_id = await self.class_table.insert_class(class_model=class_model)

            if class_id:
                return ResponseForPost(ID=class_id)

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Teacher with this ID not found!")

