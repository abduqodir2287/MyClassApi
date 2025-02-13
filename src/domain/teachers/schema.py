from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from src.domain.enums import Gender


class TeachersModel(BaseModel):
    id: int = Field(..., description="Unique identifier of the Teacher", )
    # username: str = Field(..., description="Username of the Teacher (e.g., Unique)")
    # password: Optional[str] = Field(None, description="Teacher's Password")
    firstname: Optional[str] = Field(None, description="First name of the Teacher")
    lastname: Optional[str] = Field(None, description="Last name of the Teacher")
    photo_url: Optional[str] = Field(None, description="Photo url")
    birthDate: Optional[str] = Field(None, description="The birth date of the Teacher")
    age: Optional[int] = Field(None, description="Age of the Teacher")
    gender: Optional[Gender] = Field(None, description="Gneder of the Teacher")
    subject: Optional[str] = Field(None, description="The subject that interests the Teacher")
    idol: Optional[str] = Field(None, description="Teacher's Idol")
    bio: Optional[str] = Field(None, description="Brief biography of the teacher")
    social_link: Optional[str] = Field(None, description="Teacher's social link (e.g., Instagram, Facebook ...)")
    created_at: datetime = Field(..., description="Date and time when the user was created")
    updated_at: datetime = Field(..., description="Date and time when the user was last updated")

