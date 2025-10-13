from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.response import JSendResponse, jsend_response
from app.core.db.engine import get_session
from app.modules.auth.schemas import UserResponse
from app.modules.user.services import UserService


user_router = APIRouter()


def get_user_service(session: AsyncSession = Depends(get_session)):
    return UserService(session)


@user_router.get('/', response_model=JSendResponse[list[UserResponse]])
async def list_users(service: UserService = Depends(get_user_service)):
    return jsend_response(data={'users': await service.list_users()})
