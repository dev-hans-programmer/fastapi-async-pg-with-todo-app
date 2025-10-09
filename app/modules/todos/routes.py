from fastapi import APIRouter


todo_router = APIRouter()


@todo_router.get('/')
async def list_todos():
    return {'todos': 2}
