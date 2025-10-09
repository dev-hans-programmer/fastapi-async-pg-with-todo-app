from typing import Optional
import uuid

from sqlmodel import SQLModel


class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None


class TodoRead(TodoCreate):
    id: uuid.UUID
