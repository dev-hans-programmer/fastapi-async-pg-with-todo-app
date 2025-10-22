import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.response import JSendResponse, jsend_response
from app.core.db.engine import get_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import UserResponse
from app.modules.todo.schemas import TodoCreate, TodoRead, TodoUpdate
from app.modules.todo.services import TodoService


todo_router = APIRouter()


def get_todo_service(session: AsyncSession = Depends(get_session)):
    return TodoService(session)


@todo_router.post('/', response_model=JSendResponse[list[TodoRead]])
async def create_todo(
    data: TodoCreate,
    service: TodoService = Depends(get_todo_service),
    user_details: UserResponse = Depends(get_current_user),
):
    user_id = user_details.id
    # payload = data.model_copy(update={'user_id': user_id})
    # print(f'PAYLOAD======{data} {user_details}')
    return jsend_response(
        data={'todo': await service.create_todo(data=data, user_id=user_id)}
    )


@todo_router.get('/', response_model=JSendResponse[list[TodoRead]])
async def list_todos(
    service: TodoService = Depends(get_todo_service),
    page: int = Query(1, ge=1, description='Page number'),
    limit: int = Query(10, ge=1, le=100, description='Number of todos per page'),
):
    offset = (page - 1) * limit
    todos = await service.list_todos(limit=limit, offset=offset)
    return jsend_response(data={'todos': todos})


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


@todo_router.get('/user/{user_id}', response_model=JSendResponse[list[TodoRead]])
async def get_todos_by_user(
    user_id: uuid.UUID, service: TodoService = Depends(get_todo_service)
):
    return jsend_response(data={'todos': await service.list_todos_by_user(user_id)})
