from datetime import datetime, timezone
from typing import Optional
import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


class Todo(SQLModel, table=True):
    __tablename__ = 'todos'  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=utc_now)
    )
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key='users.id')
