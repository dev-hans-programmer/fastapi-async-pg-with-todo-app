from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.utils.response import jsend_response
from app.core.logger import get_logger


class TodoException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        code: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)


def register_errors(app: FastAPI):
    logger = get_logger('custom.error.handler')

    @app.exception_handler(TodoException)
    async def todo_exception_handler(request: Request, exc: TodoException):
        logger.warning(f'TodoException: {exc.message}', exc_info=True)
        return jsend_response(
            status='fail',
            message=exc.message,
            code=exc.code,
            data=exc.data,
            http_status_code=exc.status_code,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if 400 <= exc.status_code < 500:
            logger.info(f'HTTP {exc.status_code} at {request.url.path}: {exc.detail}')
            return jsend_response(
                status='fail',
                message=exc.detail,
                data={'path': str(request.url.path)},
                http_status_code=exc.status_code,
            )
        # 5xx errors are server errors (error)
        logger.error(f'HTTP {exc.status_code} at {request.url.path}: {exc.detail}')
        return jsend_response(
            status='error',
            message='A server error occurred.',
            code='HTTP_ERROR',
            data={'path': str(request.url.path)},
            http_status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Handle Pydantic validation errors (422)"""
        logger.info(f'Validation error at {request.url.path}: {exc.errors()}')
        # Format validation errors
        errors = {}
        for error in exc.errors():
            field = '.'.join(str(loc) for loc in error['loc'][1:])  # Skip 'body'
            errors[field] = error['msg']
        return jsend_response(
            status='fail',
            message='Validation failed',
            data={'validation_errors': errors, 'path': str(request.url.path)},
            http_status_code=422,
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Catch all unhandled exceptions"""
        logger.error(f'Unhandled exception at {request.url.path}: {exc}', exc_info=True)
        # Hide raw error messages in production
        message = 'An unexpected error occurred'
        http_status_code = 500
        if isinstance(exc, IntegrityError):
            message = exc._message()
            http_status_code = 422

        return jsend_response(
            status='error',
            message=message,
            code='INTERNAL_SERVER_ERROR',
            data={'path': str(request.url.path), 'type': type(exc).__name__},
            http_status_code=http_status_code,
        )
