from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db.models.users import User
from app.modules.auth.schemas import UserCreate
from app.modules.auth.security import hash_password


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def register(self, data: UserCreate):
        # save the payload
        user = User(**data.model_dump())
        print(f'USER====== {user.password} {hash_password(user.password)}')
        user.password = hash_password(user.password)
        self.__session.add(user)
        await self.__session.commit()
        return user.id
