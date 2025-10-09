from fastapi import FastAPI

from app.api.v1.routes import api_v1_router
from app.common.utils.response import jsend_response
from app.core.logger import get_logger


logger = get_logger('Root')
app = FastAPI()


@app.get('/')
def root():
    logger.info('Root endpoint')
    return jsend_response(
        data={'message': 'Hello User, welcome to todolist server'}, message='hello'
    )


app.include_router(router=api_v1_router, prefix='/api')
