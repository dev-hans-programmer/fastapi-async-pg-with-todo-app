from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.response import JSendResponse, jsend_response
from app.core.db.engine import get_session
from app.modules.todo.schemas import TodoCreate, TodoRead, TodoUpdate
from app.modules.todo.services import TodoService


todo_router = APIRouter()


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


@todo_router.get('/{todo_id}', response_model=TodoRead)
async def get_todo(todo_id: UUID, service: TodoService = Depends(get_todo_service)):
    todo = await service.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found'
        )
    return jsend_response(data={'todo': todo})


@todo_router.patch('/{todo_id}')
async def update_todo(
    todo_id: UUID, data: TodoUpdate, service: TodoService = Depends(get_todo_service)
):
    todo = await service.update_todo(todo_id, data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found'
        )
    return jsend_response(data={'todo': todo})


@todo_router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, service: TodoService = Depends(get_todo_service)):
    deleted = await service.delete_todo(todo_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found'
        )
