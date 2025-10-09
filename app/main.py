from fastapi import FastAPI
from pydantic import BaseModel

from app.api.v1.routes import api_v1_router
from app.common.utils.response import JSendResponse, jsend_response
from app.core.logger import get_logger


logger = get_logger('Root')
app = FastAPI()


class Resp(BaseModel):
    id: int


@app.get('/', response_model=JSendResponse[Resp])
def root():
    logger.info('Root endpoint')
    return jsend_response(
        data={'message': 'Hello User, welcome to todolist server'}, message='hello'
    )


app.include_router(router=api_v1_router, prefix='/api')
