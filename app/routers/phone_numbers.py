from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.telegram import get_last_telegram_message, export_account_statistics
from app.db import get_session
from app.db.crud import get_all_telegram_accounts, get_telegram_account, create_telegram_account
from app.schemas import TelegramAccountCreate
from app.core import settings


router = APIRouter(
    prefix="/accounts",
    tags=["phone_numbers"]
)


@router.get("/")
async def telegram_accounts(session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_all_telegram_accounts(session)

@router.get("/{phone_number}")
async def telegram_account(session: Annotated[AsyncSession, Depends(get_session)], phone_number: str):
    return await get_telegram_account(session, phone_number)

@router.post("/")
async def create_account(
    session: Annotated[AsyncSession, Depends(get_session)],
    data: TelegramAccountCreate    
):
    await create_telegram_account(session, data.phone_number, settings.API_ID, settings.API_HASH, password_2fa=data.password_2fa)

    return {"status": "ok"}

@router.get("/{phone_number}/get-code")
async def get_code(session: Annotated[AsyncSession, Depends(get_session)], phone_number: str):
    phone_data = await get_telegram_account(session, phone_number)
    if not phone_data:
        raise HTTPException(status_code=404, detail="Account not found")
    data = await get_last_telegram_message(phone_data.session_string, phone_data.api_id, phone_data.api_hash)
    return {"status": "ok", "data": data}

@router.get("/{phone_number}/statistics")
async def get_statistics(session: Annotated[AsyncSession, Depends(get_session)], phone_number: str):
    phone_data = await get_telegram_account(session, phone_number)
    if not phone_data:
        raise HTTPException(status_code=404, detail="Account not found")
    data = await export_account_statistics(phone_data.session_string, phone_data.api_id, phone_data.api_hash)
    return {"status": "ok", "data": data}