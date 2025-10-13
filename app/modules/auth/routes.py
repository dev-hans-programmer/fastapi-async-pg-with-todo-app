from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.response import jsend_response
from app.core.db.engine import get_session
from app.modules.auth.schemas import UserCreate
from app.modules.auth.services import AuthService


auth_router = APIRouter()


def get_auth_service(session: AsyncSession = Depends(get_session)):
    return AuthService(session)


@auth_router.post('/')
async def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    # print(data)
    id = await service.register(data)
    return jsend_response(message='User registered', data={'id': id})
