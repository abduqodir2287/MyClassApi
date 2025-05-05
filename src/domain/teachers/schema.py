from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Optional

from src.domain.enums import Gender
from src.domain.schema import Date


class TeachersModel(BaseModel):
    username: str = Field(..., description="Username of the Teacher (e.g., Unique)")
    firstname: Optional[str] = Field(None, description="First name of the Teacher")
    lastname: Optional[str] = Field(None, description="Last name of the Teacher")
    birthDate: Optional[Date] = Field(None, description="The birth date of the Teacher")
    age: Optional[int] = Field(None, description="Age of the Teacher")
    gender: Optional[Gender] = Field(None, description="Gender of the Teacher")
    subject: Optional[str] = Field(None, description="The subject this Teacher teaches")
    idol: Optional[str] = Field(None, description="Teacher's Idol")
    bio: Optional[str] = Field(None, description="Brief biography of the teacher")
    social_link: Optional[str] = Field(None, description="Teacher's social link (e.g., Instagram, Facebook ...)")
    created_at: datetime = Field(..., description="Date and time when the Teacher was created")
    updated_at: datetime = Field(..., description="Date and time when the Teacher was last updated")

    model_config = {
        "from_attributes": True
    }


class TeachersModelForPatch(BaseModel):
    username: str = Field(..., description="Username of the Teacher (e.g., Unique)")
    password: str = Field(..., description="Password of this user")
    firstname: Optional[str] = Field(None, description="First name of the Teacher")
    lastname: Optional[str] = Field(None, description="Last name of the Teacher")
    birthDate: Optional[Date] = Field(None, description="The birth date of the Teacher")
    age: Optional[int] = Field(None, description="Age of the Teacher")
    gender: Optional[Gender] = Field(None, description="Gender of the Teacher")
    subject: Optional[str] = Field(None, description="The subject this Teacher teaches")
    idol: Optional[str] = Field(None, description="Teacher's Idol")
    bio: Optional[str] = Field(None, description="Brief biography of the teacher")
    social_link: Optional[str] = Field(None, description="Teacher's social link (e.g., Instagram, Facebook ...)")


    @model_validator(mode='before')
    def check_at_least_one_update(cls, data): # type: ignore
        updates = {k: v for k, v in data.items() if k not in {"username", "password"}}
        if not any(v is not None for v in updates.values()):
            raise ValueError("At least one field must be provided for update.")
        return data


