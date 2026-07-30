from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)
    email: EmailStr


class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str
