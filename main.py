import asyncio
import logging

from app.bot import build_dispatcher, create_bot, set_commands
from app.config import get_settings
from app.core.logging import setup_logging
from app.core.loop import configure_event_loop
from app.db.client import Database

log = logging.getLogger("main")


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    db = Database()
    await db.connect(settings.database_url.get_secret_value())

    bot = create_bot(settings)
    dp = build_dispatcher(db, settings)

    try:
        await set_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        log.info("Бот іске қосылды: @%s", me.username)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    configure_event_loop()
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Бот тоқтатылды")
