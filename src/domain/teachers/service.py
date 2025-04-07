from fastapi import HTTPException, status
from typing import Optional

from src.configs.logger_setup import logger
from src.domain.teachers.schema import TeachersModel
from src.infrastructure.database.postgres.teachers.client import TeachersTable
from src.domain.schema import Date


class TeachersRouterService:

    def __init__(self) -> None:
        self.table = TeachersTable()


    async def get_all_teachers_service(self) -> list[TeachersModel]:
        teachers_list = []
        all_teachers = await self.table.select_teachers()

        for teacher in all_teachers:
            returned_teacher = TeachersModel(
                id=teacher.id, username=teacher.username, firstname=teacher.firstname, lastname=teacher.lastname,
                birthDate=Date(date=teacher.birthDate) if teacher.birthDate is not None else teacher.birthDate, # type: ignore
                age=teacher.age, subject=teacher.subject, idol=teacher.idol, bio=teacher.bio,
                social_link=teacher.social_link, created_at=teacher.created_at, updated_at=teacher.updated_at
            )

            teachers_list.append(returned_teacher)

        return teachers_list


    async def get_teacher_by_username_service(self, username: str) -> TeachersModel:
        teacher = await self.table.select_teachers(username=username)

        if not teacher:
            logger.warning("Teacher not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher with this username not found")

        return TeachersModel(id=teacher.id, username=username, firstname=teacher.firstname, lastname=teacher.lastname,
                             birthDate=Date(date=teacher.birthDate) if teacher.birthDate is not None else None, # type: ignore
                             age=teacher.age, subject=teacher.subject, idol=teacher.idol, bio=teacher.bio,
                             social_link=teacher.social_link, created_at=teacher.created_at, updated_at=teacher.updated_at)

    async def update_teacher_info_service(
            self, username: str, password: str, firstname: Optional[str] = None,
			lastname: Optional[str] = None, birth_date: Optional[Date] = None, age: Optional[int] = None,
			subject: Optional[str] = None, idol: Optional[str] = None, bio: Optional[str] = None,
            social_link: Optional[str] = None
    ) -> TeachersModel:
        teacher = await self.table.select_teachers(username=username)

        if not teacher:
            logger.warning("Teacher not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher with this username not found")

        if birth_date is None and teacher.birthDate is not None:
            birth_date = Date(date=teacher.birthDate) # type: ignore

        elif birth_date is None and teacher.birthDate is None:
            birth_date = None

        teacher_model = TeachersModel(
            id=teacher.id, username=username, firstname=firstname if firstname is not None else teacher.firstname,
            lastname=lastname if lastname is not None else teacher.lastname, birthDate=birth_date,
            age=age if age is not None else teacher.age, subject=subject if subject is not None else teacher.subject,
            idol=idol if idol is not None else teacher.idol, bio=bio if bio is not None else teacher.bio,
            social_link=social_link if social_link is not None else teacher.social_link,
            created_at=teacher.created_at, updated_at=teacher.updated_at
        )

        update = await self.table.update_teacher_info(username, password, teacher_model)

        if update:
            return teacher_model

