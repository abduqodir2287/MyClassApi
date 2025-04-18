from src.infrastructure.database.postgres.models import Users, Students, Teachers


class UsersRouterFunctions:

    def __init__(self, users_table: Users, students_table: Students, teachers_table: Teachers) -> None:
        self.users_table = users_table
        self.students_table = students_table
        self.teachers_table = teachers_table


