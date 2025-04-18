from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ClassModel(BaseModel):
    id: int = Field(..., description="The unique id of the Class")
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    teacher_id: int = Field(..., description="The Class Teacher ID")
    school_year: str = Field(..., description="Academic year")
    class_leader_id: Optional[int] = Field(None, description="Unique class leader ID")
    description: Optional[str] = Field(None, description="Description for Class")
    class_room_number: Optional[int] = Field(None, description="Just Class room number")
    created_at: datetime = Field(..., description="Date and time when the class was created")
    updated_at: datetime = Field(..., description="Date and time when the class was last updated")


class ClassModelForPost(BaseModel):
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    teacher_id: int = Field(..., description="The Class Teacher ID")
    school_year: str = Field(..., description="Academic year")


class ClassModelForPatch(BaseModel):
    class_name: Optional[str] = Field(None, description="Name of the class (e.g 11-b, 5-a)")
    students_count: Optional[int] = Field(None, description="Number of students in a class")
    teacher_id: Optional[int] = Field(None, description="The Class Teacher ID")
    school_year: Optional[str] = Field(None, description="Academic year")
    class_leader_id: Optional[int] = Field(None, description="Unique class leader ID")
    description: Optional[str] = Field(None, description="Description for Class")
    class_room_number: Optional[int] = Field(None, description="Just Class room number")


