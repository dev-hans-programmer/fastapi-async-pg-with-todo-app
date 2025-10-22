import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    password: str
