# utils/response.py
from typing import Any, Optional

from fastapi.responses import JSONResponse

# schemas/response.py
from pydantic import BaseModel


class JSendResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None


def jsend_response(
    status: str = 'success',
    data: Optional[Any] = None,
    message: Optional[str] = None,
    http_status_code: int = 200,
) -> JSONResponse:
    payload = {'status': status}

    # Add message only if provided
    if message:
        payload['message'] = message

    # Add data (can be dict, list, etc.)
    if data is not None:
        payload['data'] = data

    return JSONResponse(content=payload, status_code=http_status_code)
