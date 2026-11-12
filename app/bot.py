from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config import Settings
from app.core.constants import THROTTLE_SECONDS
from app.db.client import Database
from app.handlers import get_root_router
from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.user import UserMiddleware


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def build_dispatcher(
    db: Database, settings: Settings, throttle_seconds: float = THROTTLE_SECONDS
) -> Dispatcher:
    # db және settings барлық хендлер мен middleware-ге dependency ретінде беріледі
    dp = Dispatcher(storage=MemoryStorage(), db=db, settings=settings)

    # Тек жеке чаттар
    dp.message.filter(F.chat.type == "private")

    for observer in (dp.message, dp.callback_query):
        observer.outer_middleware(ThrottlingMiddleware(throttle_seconds))
        observer.outer_middleware(UserMiddleware())

    dp.include_router(get_root_router())
    return dp


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Ботты бастау"),
            BotCommand(command="menu", description="Бас мәзір"),
            BotCommand(command="help", description="Көмек"),
        ]
    )
