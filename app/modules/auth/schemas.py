import uuid

from sqlmodel import Field, SQLModel


class UserCreate(SQLModel):
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=4)


class UserResponse(UserCreate):
    id: uuid.UUID
