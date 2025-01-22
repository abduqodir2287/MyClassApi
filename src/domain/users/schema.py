from pydantic import BaseModel, Field
from datetime import datetime
from src.domain.enums import UserRole


class UsersModel(BaseModel):
	id: int = Field(..., description="Unique identifier of the user", )
	username: str = Field(..., description="Username of the user (e.g., Unique)")
	password: str = Field(..., description="User's Password")
	role: UserRole = Field(..., description="Role assigned to the user (e.g., superadmin or user)")
	created_at: datetime = Field(..., description="Date and time when the user was created")
	updated_at: datetime = Field(..., description="Date and time when the user was last updated")


class UsersModelForPost(BaseModel):
	username: str = Field(..., description="Username of the user (e.g., Unique)")
	password: str = Field(..., description="User's Password")
	role: UserRole = Field(..., description="Role assigned to the user (e.g., superadmin or user)")


class UsersResponseForPost(BaseModel):
	UserId: int = Field(..., description='ID of the User')


