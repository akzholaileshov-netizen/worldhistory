"""Әлі жасалмаған бөлімдердің уақытша жауабы. Бөлім дайын болғанда сәйкес роутер
handlers/__init__.py ішінде placeholders-тен ЕЖЕЛЕ тіркеледі."""

from aiogram import F, Router
from aiogram.types import Message

from app.texts import kk


async def coming_soon(message: Message) -> None:
    await message.answer(kk.COMING_SOON.format(section=message.text, line=kk.LINE))


def create_router() -> Router:
    router = Router(name="placeholders")
    router.message.register(coming_soon, F.text.in_(kk.MENU_BUTTONS))
    return router
