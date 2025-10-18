import uuid

from sqlmodel import Field, SQLModel


class UserCreate(SQLModel):
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=4)


class UserResponse(UserCreate):
    id: uuid.UUID


class UserLoginPayload(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    access_token: str
    refresh_token: str
