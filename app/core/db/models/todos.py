from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    __tablename__ = 'todos'  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
