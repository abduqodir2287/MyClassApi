from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from src.domain.students.schema import StudentsModel
from src.domain.teachers.schema import TeachersModel


class ClassModel(BaseModel):
    id: int = Field(..., description="The unique id of the Class")
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    school_year: str = Field(..., description="Academic year")
    teacher_username: str = Field(..., description="The Class Teacher username")
    class_leader_username: Optional[str] = Field(None, description="Unique class leader username")
    description: Optional[str] = Field(None, description="Description for Class")
    class_room_number: Optional[int] = Field(None, description="Just Class room number")
    created_at: datetime = Field(..., description="Date and time when the class was created")
    updated_at: datetime = Field(..., description="Date and time when the class was last updated")

    model_config = {
        "from_attributes": True
    }


class GetFullClassInfo(BaseModel):
    id: int = Field(..., description="The unique id of the Class")
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    school_year: str = Field(..., description="Academic year")
    teacher_info: TeachersModel = Field(..., description="The Class Teacher Information")
    class_leader_info: Optional[StudentsModel] = Field(None, description="Information about Class leader")
    all_students: list[StudentsModel] = Field(..., description="All students in this class")
    description: Optional[str] = Field(None, description="Description for Class")
    class_room_number: Optional[int] = Field(None, description="Just Class room number")
    created_at: datetime = Field(..., description="Date and time when the class was created")
    updated_at: datetime = Field(..., description="Date and time when the class was last updated")


class ClassModelForPost(BaseModel):
    class_name: str = Field(..., description="Name of the class (e.g 11-b, 5-a)")
    students_count: int = Field(..., description="Number of students in a class")
    school_year: str = Field(..., description="Academic year")
    teacher_username: str = Field(..., description="The Class Teacher username")


