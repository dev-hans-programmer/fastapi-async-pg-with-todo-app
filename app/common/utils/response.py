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
    code: Optional[str] = None,
    http_status_code: int = 200,
) -> JSONResponse:
    """
        JSend response format:
    - success: status='success', data={...}
    - fail: status='fail', data={validation errors}
    - error: status='error', message='...', code='...', data={...}

    """
    payload = {'status': status}

    if status == 'success':
        if data is not None:
            payload['data'] = data
        if message:
            payload['message'] = message
    elif status == 'fail':
        if data is not None:
            payload['data'] = data
        if message:
            payload['message'] = message
    elif status == 'error':
        # Server error or application error
        payload['message'] = message or 'An error occurred'
        if code:
            payload['code'] = code
        if data is not None:
            payload['data'] = data

    return JSONResponse(content=jsonable_encoder(payload), status_code=http_status_code)
