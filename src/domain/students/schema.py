from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from src.domain.enums import Gender


class StudentsModel(BaseModel):
	id: int = Field(..., description="Unique identifier of the student", )
	# username: str = Field(..., description="Username of the student (e.g., Unique)")
	# password: str = Field(..., description="student's Password")
	firstname: Optional[str] = Field(None, description="First name of the student")
	lastname: Optional[str] = Field(None, description="Last name of the student")
	photo_url: Optional[str] = Field(None, description="Photo url")
	birthDate: Optional[str] = Field(None, description="The birth date of the Student")
	age: Optional[int] = Field(None, description="Age of the student")
	gender: Optional[Gender] = Field(None, description="Gneder of the student")
	subject: Optional[str] = Field(None, description="The subject that interests the student")
	interests: Optional[str] = Field(None, description="General interests of the student")
	idol: Optional[str] = Field(None, description="Student's Idol")
	created_at: datetime = Field(..., description="Date and time when the user was created")
	updated_at: datetime = Field(..., description="Date and time when the user was last updated")
