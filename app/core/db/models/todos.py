from datetime import datetime, timezone
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


class Todo(SQLModel, table=True):
    __tablename__ = 'todos'  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
