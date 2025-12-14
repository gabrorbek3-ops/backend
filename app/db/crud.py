from sqlalchemy import update
from sqlalchemy.future import select

from .models import TelegramAccount


async def get_telegram_account(session, phone_number: str):
    telegram_account =  await session.execute(
        select(TelegramAccount).where(TelegramAccount.phone_number == phone_number)
    )
    return telegram_account.scalars().first()

async def create_telegram_account(
    session, 
    phone_number: str, 
    api_id: int, 
    api_hash: str,
    session_string: str | None = None, 
    password_2fa: str | None = None
):
    telegram_account = TelegramAccount(
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
        password_2fa=password_2fa
    )
    session.add(telegram_account)
    await session.commit()
    await session.refresh(telegram_account)
    return telegram_account

async def get_all_telegram_accounts(session):
    telegram_accunt =  await session.execute(select(TelegramAccount))
    return telegram_accunt.scalars().all()

async def update_session_string(session, phone_number: str, session_string: str):
    await session.execute(
        update(TelegramAccount)
        .where(TelegramAccount.phone_number == phone_number)
        .values(session_string=session_string)
    )
    await session.commit()