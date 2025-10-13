from fastapi import APIRouter

from app.modules.auth import auth_router
from app.modules.todo import todo_router
from app.modules.user import user_router


api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(router=todo_router, prefix='/todos')
api_v1_router.include_router(router=auth_router, prefix='/auth')
api_v1_router.include_router(router=user_router)
