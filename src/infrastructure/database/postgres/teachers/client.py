from sqlalchemy import select
from typing import Optional

from src.domain.teachers.schema import TeachersModel
from src.infrastructure.database.postgres.models import Teachers
from src.infrastructure.database.postgres.database import Base


class TeachersTable:

    def __init__(self) -> None:
        self.table = Teachers()
        self.async_session = Base.async_session


    async def select_all_teachers(self, firstname: Optional[str] = None,
                                  lastname: Optional[str] = None) -> list[TeachersModel]:
        async with self.async_session() as session:

            if firstname is not None:
                select_user = select(Teachers).where(firstname == Teachers.firstname)

                user = await session.execute(select_user)

                return user.scalars().all()

            elif lastname is not None:
                select_user = select(Teachers).where(lastname == Teachers.lastname)

                user = await session.execute(select_user)

                return user.scalars().all()

            select_users = select(Teachers)
            all_users = await session.execute(select_users)

            return all_users.scalars().all()


    async def insert_teacher(self, username: str, password: str) -> int:
        async with self.async_session() as session:
            async with session.begin():
                insert_into = Teachers(
                    username=username,
                    password=password,
                )
                session.add(insert_into)

            await session.commit()

            await session.refresh(insert_into)

            return insert_into.id





