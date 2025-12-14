from pydantic import BaseModel, ConfigDict


class SendCode(BaseModel):
    phone: str

    model_config = ConfigDict(from_attributes=True)


class VerifyCode(BaseModel):
    phone: str
    code: str
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)