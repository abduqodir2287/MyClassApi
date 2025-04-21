from fastapi import HTTPException, status

from src.configs.logger_setup import logger
from src.domain.teachers.schema import TeachersModel, TeachersModelForPatch
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
                username=teacher.username, firstname=teacher.firstname, lastname=teacher.lastname,
                birthDate=Date(date=teacher.birthDate) if teacher.birthDate is not None else teacher.birthDate, # type: ignore
                age=teacher.age, gender=teacher.gender, subject=teacher.subject, idol=teacher.idol, bio=teacher.bio,
                social_link=teacher.social_link, created_at=teacher.created_at, updated_at=teacher.updated_at
            )

            teachers_list.append(returned_teacher)

        return teachers_list


    async def get_teacher_by_username_service(self, username: str) -> TeachersModel:
        teacher = await self.table.select_teachers(username=username)

        if not teacher:
            logger.warning("Teacher not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher with this username not found")

        return TeachersModel(
            username=username, firstname=teacher.firstname, lastname=teacher.lastname,
            birthDate=Date(date=teacher.birthDate) if teacher.birthDate is not None else None, # type: ignore
            age=teacher.age, gender=teacher.gender, subject=teacher.subject, idol=teacher.idol, bio=teacher.bio,
            social_link=teacher.social_link, created_at=teacher.created_at, updated_at=teacher.updated_at
        )

    async def update_teacher_info_service(self, teacher_model: TeachersModelForPatch) -> TeachersModel:
        teacher_info = await self.table.select_teachers(username=teacher_model.username)

        if not teacher_info:
            logger.warning("Teacher not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher with this username not found")

        if teacher_info.password != teacher_model.password:
            logger.warning("Wrong password")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are writing the wrong password."
            )

        if teacher_model.birthDate is None:
            teacher_model.birthDate = (
                Date(date=teacher_info.birthDate) if teacher_info.birthDate else None  # type: ignore
            )

        returned_teacher = TeachersModel(
            username=teacher_model.username, birthDate=teacher_model.birthDate,
            firstname=teacher_model.firstname if teacher_model.firstname is not None else teacher_info.firstname,
            lastname=teacher_model.lastname if teacher_model.lastname is not None else teacher_info.lastname,
            age=teacher_model.age if teacher_model.age is not None else teacher_info.age,
            gender=teacher_model.gender if teacher_model.gender is not None else teacher_info.gender,
            subject=teacher_model.subject if teacher_model.subject is not None else teacher_info.subject,
            idol=teacher_model.idol if teacher_model.idol is not None else teacher_info.idol,
            bio=teacher_model.bio if teacher_model.bio is not None else teacher_info.bio,
            social_link=teacher_model.social_link if teacher_model.social_link is not None else teacher_info.social_link,
            created_at=teacher_info.created_at, updated_at=teacher_info.updated_at
        )

        update = await self.table.update_teacher_info(teacher_model.username, teacher_model.password, returned_teacher)

        if update:
            return returned_teacher

