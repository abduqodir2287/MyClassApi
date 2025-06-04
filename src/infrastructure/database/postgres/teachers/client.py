from sqlalchemy import select, update, or_
from typing import Optional


from src.domain.teachers.schema import TeachersModel
from src.infrastructure.database.postgres.models import Teachers
from src.infrastructure.database.postgres.session_manager import AsyncSessionManager


class TeachersTable:

    def __init__(self) -> None:
        self.async_session = AsyncSessionManager()


    async def select_teachers(self, username: Optional[str] = None) -> list[TeachersModel] | TeachersModel:
        async with self.async_session.get_session() as session:
            if username is not None:
                select_teacher = select(Teachers).where(username == Teachers.username)

                teacher = await session.execute(select_teacher)

                return teacher.scalars().first()

            select_users = select(Teachers)
            all_users = await session.execute(select_users)

            return all_users.scalars().all()



    async def select_teachers_like(self, search_value: Optional[str] = None) -> list[TeachersModel]:
        async with self.async_session.get_session() as session:
            select_teachers = select(Teachers)

            if search_value is not None:
                select_teachers = select_teachers.where(
                    or_(
                        Teachers.username.like(f"%{search_value}%"),
                        Teachers.firstname.like(f"%{search_value}%"),
                        Teachers.lastname.like(f"%{search_value}%"),
                        Teachers.subject.like(f"%{search_value}%")
                    )
                )

            result = await session.execute(select_teachers)
            return result.scalars().all()


    async def insert_teacher(self, username: str, password: str) -> int:
        async with self.async_session.get_session_begin() as session:
            insert_into = Teachers(
                username=username,
                password=password,
            )
            session.add(insert_into)

            await session.flush()

            await session.refresh(insert_into)

            return insert_into.id


    async def update_teacher_info(self, username: str, password: str, teacher_info: TeachersModel) -> bool | None:
        async with self.async_session.get_session_begin() as session:
            update_teacher = update(Teachers).where(
                username == Teachers.username, password == Teachers.password
            ).values(
                firstname=teacher_info.firstname, lastname=teacher_info.lastname,
                birthDate=teacher_info.birthDate.date if teacher_info.birthDate is not None else None,
                age=teacher_info.age, gender=teacher_info.gender, subject=teacher_info.subject,
                idol=teacher_info.idol, bio=teacher_info.bio, social_link=teacher_info.social_link
            )

            result = await session.execute(update_teacher)
            await session.commit()

            if result.rowcount > 0:
                return True


    async def update_teacher_password(self, username: str, password: str, new_password: str) -> bool | None:
        async with self.async_session.get_session() as session:
            update_teacher = update(Teachers).where(
                username == Teachers.username, password == Teachers.password
            ).values(password=new_password)

            result = await session.execute(update_teacher)
            await session.commit()

            if result.rowcount > 0:
                return True


