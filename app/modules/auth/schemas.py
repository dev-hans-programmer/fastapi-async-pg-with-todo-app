import uuid

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str = Field(min_length=4)


class UserResponse(UserBase):
    id: uuid.UUID


class UserLoginPayload(SQLModel):
    email: str
    password: str


class LoginResponse(SQLModel):
    access_token: str
    refresh_token: str
