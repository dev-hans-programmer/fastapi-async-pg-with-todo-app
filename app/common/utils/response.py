from typing import Any, Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


T = TypeVar('T')


class JSendResponse(BaseModel, Generic[T]):
    status: str
    message: Optional[str]
    data: Optional[T] = None


def jsend_response(
    status: str = 'success',
    data: Optional[Any] = None,
    message: Optional[str] = None,
    http_status_code: int = 200,
) -> JSONResponse:
    payload = {'status': status}
    if message:
        payload['message'] = message

    if data is not None:
        payload['data'] = data

    return JSONResponse(content=jsonable_encoder(payload), status_code=http_status_code)
