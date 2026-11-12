import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.core.constants import THROTTLE_SECONDS
from app.texts import kk


class ThrottlingMiddleware(BaseMiddleware):
    """Спамнан қорғау: бір қолданушының әрекеттері арасында ең аз уақыт."""

    def __init__(self, interval: float = THROTTLE_SECONDS) -> None:
        self.interval = interval
        self._last: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        if tg_user is None:
            return await handler(event, data)

        now = time.monotonic()
        last = self._last.get(tg_user.id, 0.0)
        if now - last < self.interval:
            if isinstance(event, CallbackQuery):
                await event.answer(kk.TOO_FAST)
            elif isinstance(event, Message):
                pass  # хабарламаға үнсіз тоқтаймыз
            return None
        self._last[tg_user.id] = now

        if len(self._last) > 20000:  # жадты тазалау
            cutoff = now - 60
            self._last = {k: v for k, v in self._last.items() if v > cutoff}

        return await handler(event, data)
