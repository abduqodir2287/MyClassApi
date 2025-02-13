from src.domain.teachers.schema import TeachersModel
from src.infrastructure.database.postgres.teachers.client import TeachersTable


class TeachersRouterService:

    def __init__(self) -> None:
        self.table = TeachersTable()


    async def get_all_teachers(self) -> list[TeachersModel]:
        teachers_list = []
        all_teachers = await self.table.select_all_teachers()

        for teacher in all_teachers:
            returned_teacher = TeachersModel(
                id=teacher.id, firstname=teacher.firstname,
                lastname=teacher.lastname, photo_url=teacher.photo_url, birthDate=teacher.birthDate,
                age=teacher.age, subject=teacher.subject, idol=teacher.idol, bio=teacher.bio,
                social_link=teacher.social_link, created_at=teacher.created_at, updated_at=teacher.updated_at
            )

            teachers_list.append(returned_teacher)

        return teachers_list

