from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.payments import GetStarsStatusRequest

from app.core import settings


async def create_client(session_string: str | None = None) -> TelegramClient:
    """
    Agar session_string bo'lsa — login qilingan client
    Bo'lmasa — vaqtinchalik (send_code uchun)
    """
    session = StringSession(session_string) if session_string else StringSession()
    client = TelegramClient(session, settings.API_ID, settings.API_HASH)
    try:
        await client.connect()
    except Exception as e:
        raise e
    return client

async def get_last_telegram_message(session_string: str, api_id: int, api_hash: str):
    result = {}
    client = TelegramClient(
        StringSession(session_string),
        api_id,
        api_hash
    )

    async with client:
        messages = await client.get_messages(
            777000,
            limit=1
        )

        if not messages:
            print("Telegram'dan xabar topilmadi")
            return

        m = messages[0] # type: ignore

        result.update({
            "sana": m.date,
            "matn": m.text,
            "id": m.id
        })

    return result

async def export_account_statistics(session_string: str, api_id: int, api_hash: str):
    client = TelegramClient(
        StringSession(session_string),
        api_id,
        api_hash
    )

    stats = {
        "account": {
            "user_id": None,
            "username": None,
            "phone": None,
            "is_premium": False,
            "is_verified": False,
            "is_scam": False,
            "is_fake": False,
            "stars_balance": 0
        },
        "dialogs_stats": {
            "total_dialogs": 0,
            "groups": 0,
            "channels": 0,
            "private_chats": 0,
            "admin_in": 0,
            "owner_in": 0,
            "read_only": 0,
        },
        "dialogs": []
    }

    async with client:
        # 👤 ACCOUNT INFO
        me = await client.get_me()
        full = await client(GetFullUserRequest(me.id))

        stats["account"].update({
            "user_id": me.id,
            "username": me.username,
            "phone": me.phone,
            "is_premium": bool(me.premium),
            "is_verified": bool(me.verified),
            "is_scam": bool(me.scam),
            "is_fake": bool(me.fake),
        })

        # ⭐ STARS
        try:
            stars = await client(GetStarsStatusRequest(peer=me))
            stats["account"]["stars_balance"] = stars.balance.amount
        except Exception:
            stats["account"]["stars_balance"] = 0

        # 💬 DIALOGS
        async for dialog in client.iter_dialogs():
            stats["dialogs_stats"]["total_dialogs"] += 1
            entity = dialog.entity

            dialog_data = {
                "id": dialog.id,
                "name": dialog.name,
                "type": None,
                "is_admin": False,
                "is_owner": False,
                "is_read_only": False,
                "is_broadcast": False,
                "members_count": None,
            }

            # PRIVATE
            if dialog.is_user:
                stats["dialogs_stats"]["private_chats"] += 1
                dialog_data["type"] = "private"

            # GROUP
            elif dialog.is_group:
                stats["dialogs_stats"]["groups"] += 1
                dialog_data["type"] = "group"

                if (
                    hasattr(entity, "default_banned_rights")
                    and entity.default_banned_rights
                    and entity.default_banned_rights.send_messages
                ):
                    dialog_data["is_read_only"] = True
                    stats["dialogs_stats"]["read_only"] += 1

            # CHANNEL
            elif dialog.is_channel:
                stats["dialogs_stats"]["channels"] += 1
                dialog_data["type"] = "channel"

                if getattr(entity, "broadcast", False):
                    dialog_data["is_broadcast"] = True
                    dialog_data["is_read_only"] = True
                    stats["dialogs_stats"]["read_only"] += 1

            # OWNER
            if getattr(entity, "creator", False):
                dialog_data["is_owner"] = True
                stats["dialogs_stats"]["owner_in"] += 1

            # ADMIN
            if getattr(entity, "admin_rights", None):
                dialog_data["is_admin"] = True
                stats["dialogs_stats"]["admin_in"] += 1

            # MEMBERS COUNT (agar mavjud bo‘lsa)
            if hasattr(entity, "participants_count"):
                dialog_data["members_count"] = entity.participants_count

            stats["dialogs"].append(dialog_data)

    return stats

    
