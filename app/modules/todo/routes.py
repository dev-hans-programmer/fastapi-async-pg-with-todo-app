from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.response import JSendResponse, jsend_response
from app.core.db.engine import get_session
from app.modules.todo.schemas import TodoCreate, TodoRead
from app.modules.todo.services import TodoService


todo_router = APIRouter()

todos = [{'id': 1, 'title': 'Hello todo'}]


def get_todo_service(session: AsyncSession = Depends(get_session)):
    return TodoService(session)


@todo_router.post('/', response_model=JSendResponse[TodoRead])
async def create_todo(
    data: TodoCreate, service: TodoService = Depends(get_todo_service)
):
    return jsend_response(data={'todo': await service.create_todo(data)})


@todo_router.get('/', response_model=JSendResponse[TodoRead])
async def list_todos(service: TodoService = Depends(get_todo_service)):
    return jsend_response(data={'todos': await service.list_todos()})
