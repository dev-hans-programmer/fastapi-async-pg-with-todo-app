from fastapi import APIRouter


auth_router = APIRouter()


@auth_router.get('/me')
async def get_me():
    return {'me': 'ok'}
