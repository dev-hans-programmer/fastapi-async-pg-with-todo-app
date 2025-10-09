from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db.models.todos import Todo
from app.modules.todo.schemas import TodoCreate


class TodoService:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create_todo(self, data: TodoCreate):
        todo = Todo(**data.model_dump())
        self.__session.add(todo)
        await self.__session.commit()
        await self.__session.refresh(todo)
        return todo

    async def list_todos(self):
        result = await self.__session.exec(select(Todo))
        return result.all()
