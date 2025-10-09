from fastapi import APIRouter

from app.common.utils.response import JSendResponse, jsend_response
from app.modules.todo.schemas import TodoRead


todo_router = APIRouter()

todos = [{'id': 1, 'title': 'Hello todo'}]


@todo_router.get('/', response_model=JSendResponse[TodoRead])
async def list_todos():
    return jsend_response(data={'todos': todos})
