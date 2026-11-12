from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.config import Settings
from app.db.client import Database
from app.db.repositories.users import UserRepository
from app.texts import kk


class UserMiddleware(BaseMiddleware):
    """Әр update үшін қолданушыны базада табады/жасайды және data['user'] ішіне салады."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        if tg_user is None or tg_user.is_bot:
            return await handler(event, data)

        db: Database = data["db"]
        settings: Settings = data["settings"]
        user = await UserRepository(db).upsert_from_telegram(
            tg_id=tg_user.id,
            username=tg_user.username,
            full_name=tg_user.full_name,
            default_subject=settings.default_subject,
        )

        if user.is_banned:
            if isinstance(event, Message):
                await event.answer(kk.BANNED)
            elif isinstance(event, CallbackQuery):
                await event.answer(kk.BANNED, show_alert=True)
            return None

        data["user"] = user
        return await handler(event, data)
