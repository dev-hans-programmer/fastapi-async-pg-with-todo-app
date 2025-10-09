import asyncio

from app.core.db.engine import init_db


asyncio.run(init_db())
