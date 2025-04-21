from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Optional


class ClassModel(BaseModel):
    id: int = Field(..., description="The unique id of the Class")
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    teacher_username: str = Field(..., description="The Class Teacher username")
    school_year: str = Field(..., description="Academic year")
    class_leader_username: Optional[str] = Field(None, description="Unique class leader username")
    description: Optional[str] = Field(None, description="Description for Class")
    class_room_number: Optional[int] = Field(None, description="Just Class room number")
    created_at: datetime = Field(..., description="Date and time when the class was created")
    updated_at: datetime = Field(..., description="Date and time when the class was last updated")


class ClassModelForPost(BaseModel):
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    teacher_username: str = Field(..., description="The Class Teacher username")
    school_year: str = Field(..., description="Academic year")


