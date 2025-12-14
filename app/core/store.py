import asyncio
import time
from typing import Dict, Optional
from telethon import TelegramClient


class _ClientEntry:
    __slots__ = ("client", "expires_at")

    def __init__(self, client: TelegramClient, ttl: int | None):
        self.client = client
        self.expires_at = time.monotonic() + ttl if ttl else None


class TelegramClientStore:
    def __init__(self, cleanup_interval: int = 5):
        self._store: Dict[str, _ClientEntry] = {}
        self._lock = asyncio.Lock()
        self._cleanup_interval = cleanup_interval
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        if not self._task:
            self._task = asyncio.create_task(self._cleanup_loop())

    async def stop(self):
        if self._task:
            self._task.cancel()
            self._task = None

    async def set(self, key: str, client: TelegramClient, ttl: int | None = None):
        async with self._lock:
            self._store[key] = _ClientEntry(client, ttl)

    async def get(self, key: str) -> Optional[TelegramClient]:
        async with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None

            if entry.expires_at and entry.expires_at <= time.monotonic():
                await self._delete_nolock(key)
                return None

            return entry.client

    async def delete(self, key: str):
        async with self._lock:
            await self._delete_nolock(key)

    async def _delete_nolock(self, key: str):
        entry: Optional[_ClientEntry] = self._store.pop(key, None)
        if entry is not None:
            try:
                await entry.client.disconnect()
            except Exception:
                pass

    async def _cleanup_loop(self):
        try:
            while True:
                await asyncio.sleep(self._cleanup_interval)
                now = time.monotonic()
                async with self._lock:
                    expired = [
                        k for k, v in self._store.items()
                        if v.expires_at and v.expires_at <= now
                    ]
                    for key in expired:
                        await self._delete_nolock(key)
        except asyncio.CancelledError:
            pass

store = TelegramClientStore()
