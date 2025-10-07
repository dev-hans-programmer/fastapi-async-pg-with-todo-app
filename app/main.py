from fastapi import FastAPI

from app.common.utils.response import JSendResponse, jsend_response
from app.core.logger import get_logger


logger = get_logger('Root')
app = FastAPI()


@app.get('/', response_model=JSendResponse)
def root():
    logger.info('Root endpoint')
    return jsend_response(
        data={'message': 'Hello User, welcome to todolist server'},
    )
