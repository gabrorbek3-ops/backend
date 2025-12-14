from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError
)
from telethon.tl.functions.auth import ResetAuthorizationsRequest

from app.core import settings, redis, store
from app.telegram.client import create_client


API_ID = settings.API_ID
API_HASH = settings.API_HASH

async def send_code(phone: str):
    """
    Telefon raqamga Telegram login kodi yuboradi
    """
    client = await create_client()
    response = await client.send_code_request(phone)

    await redis.set(f"phone{phone}", response.phone_code_hash, ex=300)
    await store.set(phone, client, 300)

async def verify_code(phone: str, code: str, password: str | None = None):
    code_hash = await redis.get(f"phone{phone}")
    if not code_hash:
        raise ValueError("Kod yuborilmagan yoki eskirgan")

    client = await store.get(phone)
    if client is None:
        raise ValueError("Sessiya eskirgan yoki yaratilmagan")

    try:
        await client.sign_in(
            phone=phone,
            code=code,
            phone_code_hash=code_hash
        )

    except PhoneCodeExpiredError:
        await redis.delete(f"phone{phone}")
        raise Exception("Kod eskirgan, qaytadan yuboring")

    except PhoneCodeInvalidError:
        raise Exception("Kod noto‘g‘ri")

    except SessionPasswordNeededError:
        if not password:
            raise Exception("2FA parol kerak")
        await client.sign_in(password=password)

    session_string = client.session.save() # type: ignore
    await redis.delete(f"phone{phone}")
    client.disconnect()

    return session_string

async def logout_other_sessions(session_string: str):
    client = TelegramClient(
        StringSession(session_string),
        API_ID,
        API_HASH
    )
    client.start()

    await client(ResetAuthorizationsRequest())

    client.disconnect()
