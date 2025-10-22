from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.errors import TodoException
from app.common.utils.response import JSendResponse, jsend_response
from app.core.db.engine import get_session
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import (
    LoginResponse,
    UserCreate,
    UserLoginPayload,
    UserResponse,
)
from app.modules.auth.security import create_token, verify_password
from app.modules.auth.services import AuthService
from app.modules.user.services import UserService


auth_router = APIRouter()


def get_auth_service(session: AsyncSession = Depends(get_session)):
    return AuthService(session)


def get_user_service(session: AsyncSession = Depends(get_session)):
    return UserService(session)


@auth_router.post('/')
async def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    # print(data)
    id = await service.register(data)
    return jsend_response(message='User registered', data={'id': id})


@auth_router.post('/login', response_model=JSendResponse[LoginResponse])
async def login(
    data: UserLoginPayload, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_email(data.email)

    if not user:
        raise TodoException(status.HTTP_401_UNAUTHORIZED, message='Unauthorized')

    is_match = verify_password(data.password, user.password)

    if not is_match:
        raise TodoException(status.HTTP_401_UNAUTHORIZED, message='Unauthorized')

    payload = {
        'email': data.email,
        'id': str(user.id),
    }  # making this uuid to str in necessary otherwise
    # jwt will not be able to serialise this

    access_token = create_token(user_data=payload)
    refresh_token = create_token(user_data=payload, refresh=True)
    return jsend_response(
        message='Login Successful',
        data={'access_token': access_token, 'refresh_token': refresh_token},
    )
    # Generate access token and refresh token
    # send to the client


@auth_router.get('/self', response_model=JSendResponse[UserResponse])
async def get_me(user_details=Depends(get_current_user)):
    return jsend_response(data={'user': user_details})
