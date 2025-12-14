from fastapi import APIRouter, Request

from app.telegram import send_code, verify_code
from app.utils import is_valid_phone
from app.db.session import LocalAsyncSession
from app.db.crud import create_telegram_account
from app.core import settings
from app.schemas import SendCode, VerifyCode

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/send-code")
async def send_code_route(request_data: SendCode):
    data = request_data.model_dump()
    phone = data.get("phone")
    if not phone:
        return {"status": "error", "detail": "Telefon raqamni kiriting"}
    if not is_valid_phone(phone):
        return {"status": "error", "detail": "Telefon raqam noto'g'ri"}
    await send_code(phone)
    return {"status": "ok"}

@router.post("/verify-code")
async def verify_code_route(request_data: VerifyCode):
    data = request_data.model_dump()
    phone = data.get("phone")
    if not phone:
        return {"status": "error", "detail": "Telefon raqamni kiriting"}
    code = data.get("code")
    if not code:
        return {"status": "error", "detail": "Kodni kiriting"}
    password = data.get("password")
    try:
        session_string = await verify_code(phone, code, password)
        async with LocalAsyncSession() as session:
            await create_telegram_account(session, phone, settings.API_ID, settings.API_HASH, session_string, password)
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    return {"status": "ok", "session_string": session_string}