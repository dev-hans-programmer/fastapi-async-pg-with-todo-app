from fastapi import Depends, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.utils.errors import TodoException
from app.core.db.engine import get_session
from app.modules.auth.schemas import UserResponse
from app.modules.auth.security import decode_token
from app.modules.user.services import UserService


def get_user_service(session: AsyncSession = Depends(get_session)):
    return UserService(session)


class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        if not creds:
            raise TodoException(
                status_code=status.HTTP_403_FORBIDDEN, message='Unauthorized'
            )

        return creds


http_bearer_scheme = AccessTokenBearer()


async def decode_tokens(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer_scheme),
    is_access_token: bool = True,
):
    token_data = decode_token(creds.credentials)
    if not token_data:
        raise TodoException(status.HTTP_401_UNAUTHORIZED, message='Unauthorized')

    # TODO: have a check to see whether the jti is revoked or not

    if is_access_token and token_data.get('refresh'):
        raise TodoException(
            status.HTTP_403_FORBIDDEN, message='Access token required, not refresh'
        )

    if not is_access_token and not token_data.get('refresh'):
        raise TodoException(
            status.HTTP_403_FORBIDDEN, message='Refresh token required, not access'
        )
    return token_data


async def decode_access_token(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer_scheme),
):
    return await decode_tokens(creds, is_access_token=True)


async def decode_refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer_scheme),
):
    return await decode_tokens(creds, is_access_token=False)


async def get_current_user(
    token_data=Depends(decode_access_token),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user_by_email(token_data['user']['email'])

    if not user:
        raise TodoException(status.HTTP_401_UNAUTHORIZED, message='Unauthorized')

    # del user.password # this is harmful as it deleted the field from the session
    return UserResponse.model_validate(user)
