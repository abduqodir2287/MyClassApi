from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

from src.domain.enums import Gender
from src.domain.schema import Date

class StudentsModel(BaseModel):
	username: str = Field(..., description="Username of the student (e.g., Unique)")
	class_id: int = Field(..., description="Unique identifier of the class this student is in")
	firstname: Optional[str] = Field(None, description="First name of the student")
	lastname: Optional[str] = Field(None, description="Last name of the student")
	birthDate: Optional[Date] = Field(None, description="The birth date of the Student")
	age: Optional[int] = Field(None, description="Age of the student")
	gender: Optional[Gender] = Field(None, description="Gender of the student")
	subject: Optional[str] = Field(None, description="The subject that interests the student")
	interests: Optional[str] = Field(None, description="General interests of the student")
	idol: Optional[str] = Field(None, description="Student's Idol")
	bio: Optional[str] = Field(None, description="Brief biography of the teacher")
	social_link: Optional[str] = Field(None, description="Teacher's social link (e.g., Instagram, Facebook ...)")
	created_at: datetime = Field(..., description="Date and time when the user was created")
	updated_at: datetime = Field(..., description="Date and time when the user was last updated")


class StudentsModelForPatch(BaseModel):
	username: str = Field(..., description="Username of the student (e.g., Unique)", min_length=3, max_length=50)
	password: str = Field(..., description="Password of this user", min_length=8, max_length=50)
	firstname: Optional[str] = Field(None, description="First name of the student")
	lastname: Optional[str] = Field(None, description="Last name of the student")
	birthDate: Optional[Date] = Field(None, description="The birth date of the Student")
	age: Optional[int] = Field(None, description="Age of the student")
	gender: Optional[Gender] = Field(None, description="Gender of the student")
	subject: Optional[str] = Field(None, description="The subject that interests the student")
	interests: Optional[str] = Field(None, description="General interests of the student")
	idol: Optional[str] = Field(None, description="Student's Idol")
	bio: Optional[str] = Field(None, description="Brief biography of the teacher")
	social_link: Optional[str] = Field(None, description="Teacher's social link (e.g., Instagram, Facebook ...)")


	@model_validator(mode='before')
	def check_at_least_one_update(cls, data): # type: ignore
		updates = {k: v for k, v in data.items() if k not in {"username", "password"}}
		if not any(v is not None for v in updates.values()):
			raise ValueError("At least one field must be provided for update.")
		return data


