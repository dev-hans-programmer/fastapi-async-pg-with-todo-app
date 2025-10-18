from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db.models.users import User


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def list_users(self):
        result = await self.__session.exec(select(User))
        return result.all()

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await self.__session.exec(statement)
        return result.first()
