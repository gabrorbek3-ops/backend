from pydantic import BaseModel, ConfigDict


class TelegramAccountCreate(BaseModel):
    phone_number: str
    password_2fa: str
    session_string: str | None

    model_config = ConfigDict(from_attributes=True)