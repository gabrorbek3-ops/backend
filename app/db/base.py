from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core import settings


engine = create_async_engine(settings.DB_URL, echo=True)

LocalAsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass