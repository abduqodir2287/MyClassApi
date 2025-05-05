from pydantic import BaseModel, Field
from datetime import datetime

from src.domain.enums import UserRole


class UsersModel(BaseModel):
	id: int = Field(..., description="Unique identifier of the user", )
	username: str = Field(..., description="Username of the user (e.g., Unique)")
	password: str = Field(..., description="User's Password")
	role: UserRole = Field(..., description="Role assigned to the user (e.g., superadmin, teacher, student or user)")
	created_at: datetime = Field(..., description="Date and time when the user was created")
	updated_at: datetime = Field(..., description="Date and time when the user was last updated")

	model_config = {
		"from_attributes": True
	}


class UsersModelForGet(BaseModel):
	id: int = Field(..., description="Unique identifier of the user", )
	username: str = Field(..., description="Username of the user (e.g., Unique)")
	role: UserRole = Field(..., description="Role assigned to the user (e.g., superadmin, teacher, student or user)")
	created_at: datetime = Field(..., description="Date and time when the user was created")
	updated_at: datetime = Field(..., description="Date and time when the user was last updated")

	model_config = {
		"from_attributes": True
	}


class AddUserModel(BaseModel):
	username: str = Field(..., description="Username of the user (e.g., Unique)", min_length=3, max_length=50)
	password: str = Field(..., description="User's Password", min_length=5, max_length=50)
	role: UserRole = Field(..., description="Role assigned to the user (e.g., superadmin, teacher, student or user)")


class UsersModelForPost(BaseModel):
	username: str = Field(..., description="Username of the user (e.g., Unique)", min_length=3, max_length=50)
	password: str = Field(..., description="User's Password", min_length=5, max_length=50)


class UsersModelForPatch(BaseModel):
	username: str = Field(..., description="Username of the user", min_length=3, max_length=50),
	password: str = Field(..., description="User's Password", min_length=5, max_length=50),
	new_username: str = Field(..., description="New Username of the user", min_length=3, max_length=50)


class ChangePasswordModel(BaseModel):
	username: str = Field(..., description="Username of the user", min_length=3, max_length=50),
	password: str = Field(..., description="User's Password", min_length=5, max_length=50),
	new_password: str = Field(..., description="User's Password", min_length=5, max_length=50)

class UsersStudentModel(BaseModel):
	username: str = Field(..., description="Username of the user (e.g., Unique)", min_length=3, max_length=50)
	password: str = Field(..., description="User's Password", min_length=5, max_length=50)
	class_id: int = Field(..., description="Unique identifier of the class this student is in")


class AuthorizedUser(BaseModel):
	Result: str = Field(..., description="Result of the authorization process")


