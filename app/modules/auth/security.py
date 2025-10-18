from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from passlib.context import CryptContext

from app.core.config import settings


ACCESS_TOKEN_EXPIRY = 60 * 60
REFRESH_TOKEN_EXPIRY = 365 * 24 * 60 * 60


pwd_context = CryptContext(schemes=['sha256_crypt'])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(str_password: str, password: str):
    return pwd_context.verify(str_password, password)


def create_token(
    user_data: dict, expiry: timedelta | None = None, refresh: bool = False
):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (
        expiry
        if expiry is not None
        else timedelta(seconds=REFRESH_TOKEN_EXPIRY if refresh else ACCESS_TOKEN_EXPIRY)
    )

    payload['jti'] = str(uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError:
        return None
