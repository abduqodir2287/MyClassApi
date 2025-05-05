from typing import Optional
from sqlalchemy import select, update

from src.infrastructure.database.postgres.session_manager import AsyncSessionManager
from src.infrastructure.database.postgres.models import Class
from src.domain.course.schema import ClassModel, ClassModelForPost


class ClassTable:

    def __init__(self) -> None:
        self.table = Class()
        self.async_session = AsyncSessionManager()



    async def select_classes(self, class_id: Optional[int] = None,
                             class_name: Optional[str] = None) -> list[ClassModel] | ClassModel:
        async with self.async_session.get_session() as session:

            if class_name is not None:
                select_class = select(Class).where(class_name == Class.class_name)

                stmt = await session.execute(select_class)

                return stmt.scalars().first()

            elif class_id is not None:
                select_class = select(Class).where(class_id == Class.id)

                stmt = await session.execute(select_class)

                return stmt.scalars().first()

            select_classes = select(Class)
            all_classes = await session.execute(select_classes)

            return all_classes.scalars().all()



    async def select_class_like(self, class_name: Optional[str] = None) -> list[ClassModel]:
        async with self.async_session.get_session() as session:
            select_classes = select(Class)

            if class_name is not None:
                select_classes = select_classes.where(Class.class_name.like(f"%{class_name}%"))

            result = await session.execute(select_classes)
            return result.scalars().all()


    async def insert_class(self, class_model: ClassModelForPost) -> int:
        async with self.async_session.get_session_begin() as session:
            insert_into = Class(
                class_name=class_model.class_name, students_count=class_model.students_count,
                teacher_username=class_model.teacher_username, school_year=class_model.school_year
            )
            session.add(insert_into)

            await session.flush()

            await session.refresh(insert_into)

            return insert_into.id


    async def update_class_info(self, class_model: ClassModel) -> bool | None:
        async with self.async_session.get_session_begin() as session:
            update_class = update(Class).where(
                class_model.class_name == Class.class_name).values(
                students_count=class_model.students_count, school_year=class_model.school_year,
                class_leader_username=class_model.class_leader_username, description=class_model.description,
                class_room_number=class_model.class_room_number
            )

            result = await session.execute(update_class)
            await session.commit()

            if result.rowcount > 0:
                return True




