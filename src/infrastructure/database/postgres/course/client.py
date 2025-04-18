from typing import Optional
from sqlalchemy import select

from src.infrastructure.database.postgres.database import Base
from src.infrastructure.database.postgres.models import Class
from src.domain.course.schema import ClassModel, ClassModelForPost


class ClassTable:

    def __init__(self) -> None:
        self.table = Class()
        self.async_session = Base.async_session



    async def select_classes(self, class_id: Optional[int] = None,
                             class_name: Optional[str] = None) -> list[ClassModel] | ClassModel:
        async with self.async_session() as session:

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


    async def insert_class(self, class_model: ClassModelForPost) -> int:
        async with self.async_session() as session:
            async with session.begin():
                insert_into = Class(
                    class_name=class_model.class_name, students_count=class_model.students_count,
                    teacher_id=class_model.teacher_id, school_year=class_model.school_year
                )
                session.add(insert_into)

            await session.commit()

            await session.refresh(insert_into)

            return insert_into.id


