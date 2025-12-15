import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Text,
    TIMESTAMP,
    text
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        doc="+998901234567 format"
    )

    api_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    api_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    session_string: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Telethon / Pyrogram StringSession"
    )

    password_2fa: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="ENCRYPTED two-step verification password"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="sotilmagan",
        server_default=text("'sotilmagan'"),
        nullable=False,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("1"),
        nullable=False
    )

    is_banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("0"),
        nullable=False
    )

    last_login_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    last_used_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    error_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )

    price: Mapped[int] = mapped_column(
        Integer,
        default=30,
        server_default=text("30"),
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<TelegramAccount "
            f"id={self.id} "
            f"phone={self.phone_number} "
            f"active={self.is_active}>"
        )
