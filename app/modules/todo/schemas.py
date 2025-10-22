from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel

from app.modules.auth.schemas import UserResponse


class APIBaseSchema(BaseModel):
    # This configuration is inherited by all subclasses
    model_config = ConfigDict(from_attributes=True)


class TodoCreate(APIBaseSchema):
    title: str
    description: Optional[str] = None


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TodoRead(TodoCreate):
    id: uuid.UUID
    created_at: datetime


class TodoWithUser(TodoRead):
    user: Optional[UserResponse]
