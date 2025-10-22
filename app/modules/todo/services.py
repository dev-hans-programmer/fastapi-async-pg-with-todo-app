from typing import Optional
import uuid

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db.models.todos import Todo
from app.modules.todo.schemas import TodoCreate, TodoUpdate, TodoWithUser


class TodoService:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create_todo(self, data: TodoCreate, user_id: uuid.UUID):
        todo = Todo(**data.model_dump(), user_id=user_id)
        self.__session.add(todo)
        await self.__session.commit()
        await self.__session.refresh(todo)
        return todo

    async def list_todos(self, limit: int = 10, offset: int = 0):
        stmt = select(Todo).offset(offset).limit(limit).options(selectinload(Todo.user))
        result = await self.__session.exec(stmt)
        return [TodoWithUser.model_validate(todo) for todo in result.all()]

    async def list_todos_by_user(self, user_id: uuid.UUID):
        statement = select(Todo).where(Todo.user_id == user_id)
        result = await self.__session.exec(statement)
        return result.all()

    async def get_todo(self, todo_id: uuid.UUID):
        result = await self.__session.exec(
            select(Todo).where(Todo.id == todo_id).options(selectinload(Todo.user))
        )
        todo = result.first()
        if todo:
            print(f'USER====={todo.user}')
        return TodoWithUser.model_validate(todo)

    async def update_todo(
        self, todo_id: uuid.UUID, data: TodoUpdate
    ) -> Optional[TodoWithUser]:
        todo = await self.get_todo(todo_id)

        if not todo:
            return None

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(todo, k, v)
        self.__session.add(todo)
        await self.__session.commit()
        await self.__session.refresh(todo)
        return todo

    async def delete_todo(self, todo_id: uuid.UUID) -> bool:
        todo = await self.get_todo(todo_id)
        if not todo:
            return False
        await self.__session.delete(todo)
        await self.__session.commit()
        return True
