from enum import Enum

class UserRole(str, Enum):
	user = "user"
	student = "student"
	teacher = "teacher"
	superadmin = "superadmin"
