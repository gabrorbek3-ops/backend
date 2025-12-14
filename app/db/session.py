from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator

from .base import LocalAsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with LocalAsyncSession() as session:
        yield session
