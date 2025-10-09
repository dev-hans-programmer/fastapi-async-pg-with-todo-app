from typing import Optional
import uuid

from sqlmodel import SQLModel


class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TodoRead(TodoCreate):
    id: uuid.UUID
