from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.dialects.mysql import insert

from datetime import datetime, timezone

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
    data = {
        "phone_number": phone_number,
        "api_id": api_id,
        "api_hash": api_hash,
        "session_string": session_string,
        "password_2fa": password_2fa,
        "updated_at": datetime.now(timezone.utc),
    }

    data = {key: value for key, value in data.items() if value is not None}

    stmt = insert(TelegramAccount).values(**data)

    stmt = stmt.on_duplicate_key_update(
        api_id=stmt.inserted.api_id,
        api_hash=stmt.inserted.api_hash,
        session_string=stmt.inserted.session_string,
        password_2fa=stmt.inserted.password_2fa,
        updated_at=datetime.now(timezone.utc),
    )

    await session.execute(stmt)
    await session.commit()

    result = await session.execute(
        select(TelegramAccount)
        .where(TelegramAccount.phone_number == phone_number)
    )
    return result.scalar_one()


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

async def update_status(session, phone_number: str, status: str):
    await session.execute(
        update(TelegramAccount)
        .where(TelegramAccount.phone_number == phone_number)
        .values(status=status)
    )
    await session.commit()