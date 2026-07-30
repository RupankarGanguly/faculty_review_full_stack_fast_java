from pydantic import BaseModel, Field


class Faculty(BaseModel):
    Name: str = Field(..., min_length=1)
    Designation: str = Field(..., min_length=1)
    Review: str = Field(..., min_length=1)


class FacultyResponseSchema(BaseModel):
    id: int
    Name: str
    Designation: str
    Review: str
    user_id: int

    class Config:
        from_attributes = True
