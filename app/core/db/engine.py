from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings


async_engine: AsyncEngine = create_async_engine(url=settings.DB_URL, echo=True)


async_session_maker = sessionmaker(
    bind=async_engine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore


async def get_session():
    async with async_session_maker() as session:  # type: ignore
        yield session


async def init_db():
    from app.core.db import models  # noqa

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
