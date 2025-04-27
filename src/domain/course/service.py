from typing import Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError

from src.domain.course.functions import ClassRouterFunctions
from src.domain.teachers.service import TeachersRouterService
from src.infrastructure.authentication.service import get_token
from src.domain.course.schema import ClassModel, ClassModelForPost, GetFullClassInfo
from src.domain.schema import ResponseForPost
from src.infrastructure.database.postgres.course.client import ClassTable
from src.infrastructure.database.postgres.students.client import StudentsTable


class ClassRouterService(ClassRouterFunctions, TeachersRouterService):

    def __init__(self) -> None:
        self.class_table = ClassTable()
        self.students_table = StudentsTable()

        super().__init__(students_table=self.students_table)
        TeachersRouterService.__init__(self)


    async def get_all_classes_service(self, class_name: Optional[str] = None) -> list[ClassModel]:
        all_classes = []

        for course in await self.class_table.select_class_like(class_name):

            all_classes.append(await self.class_model_formatter(
                course.id, course.class_name, course.teacher_username, course.students_count, course.school_year,
                course.class_leader_username, course.description, course.class_room_number, course.created_at,
                course.updated_at
            ))

        return all_classes



    async def get_full_class_info_service(self, class_name: str) -> GetFullClassInfo:
        class_info = await self.class_table.select_classes(class_name=class_name)

        await self.check_resource(resource=class_info, detail="Class not found")

        teacher_info = await self.get_teacher_by_username_service(class_info.teacher_username)

        class_l_info = None

        if class_info.class_leader_username:
            class_l_info = await self.get_student_by_username_service(class_info.class_leader_username)

        all_students = await self.get_all_students_service(class_id=class_info.id)

        return GetFullClassInfo(
            id=class_info.id, class_name=class_name, students_count=class_info.students_count, all_students=all_students,
            teacher_info=teacher_info, class_leader_info=class_l_info, school_year=class_info.school_year,
            description=class_info.description, class_room_number=class_info.class_room_number,
            created_at=class_info.created_at, updated_at=class_info.updated_at
        )



    async def add_class_service(self, class_name: str, students_count: int, teacher_username: str, school_year: str,
                                token: str = Depends(get_token)) -> ResponseForPost:
        try:
            await self.check_role_teacher_and_superadmin(token)

            class_model = ClassModelForPost(class_name=class_name, students_count=students_count,
                                            teacher_username=teacher_username, school_year=school_year)

            class_id = await self.class_table.insert_class(class_model=class_model)

            if class_id:
                return ResponseForPost(ID=class_id)

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher with this username not found!")



    async def update_class_info_service(
            self, class_name: str, students_count: Optional[int] = None, school_year: Optional[str] = None,
            class_leader_username: Optional[str] = None, description: Optional[str] = None,
            class_room_number: Optional[int] = None, token: str = Depends(get_token)
    ) -> ClassModel | None:
        await self.check_role_teacher_and_superadmin(token)

        class_info = await self.class_table.select_classes(class_name=class_name)

        await self.check_resource(class_info, "Class with this class name not found")

        if all(value is None for value in
               [students_count, school_year, class_leader_username, description, class_room_number]):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update."
            )

        await self.check_class_leader(class_info.id, class_leader_username)

        class_model = await self.class_model_formatter(
            class_info.id, class_name, class_info.teacher_username,
            students_count if students_count is not None else class_info.students_count,
            school_year if school_year is not None else class_info.school_year,
            class_leader_username if class_leader_username is not None else class_info.class_leader_username,
            description if description is not None else class_info.description,
            class_room_number if class_room_number is not None else class_info.class_room_number,
            class_info.created_at, class_info.updated_at
        )

        update = await self.class_table.update_class_info(class_model)

        if update:
            return class_model



