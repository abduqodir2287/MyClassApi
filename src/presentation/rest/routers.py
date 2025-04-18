from src.presentation.rest.students.router import students_router
from src.presentation.rest.users.router import users_router
from src.presentation.rest.teachers.router import teachers_router
from src.presentation.rest.course.router import class_router

all_routers = [
	users_router,
	students_router,
	teachers_router,
	class_router
]
