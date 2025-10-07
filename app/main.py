from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.core.logger import get_logger


logger = get_logger('Root')
app = FastAPI()


@app.get('/')
def root():
    logger.info('Root endpoint')
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Hello User, welcome to todolist server'},
    )
