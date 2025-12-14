from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated

from app.db import get_session


router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
async def health():
    return {"status": "ok"}

@router.get("/db")
async def db(
    session: Annotated[AsyncSession, Depends(get_session)]
) :
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}