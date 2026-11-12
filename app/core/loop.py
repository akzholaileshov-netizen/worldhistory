import asyncio
import sys


def configure_event_loop() -> None:
    """psycopg async Windows-та ProactorEventLoop-пен жұмыс істемейді, Selector қажет."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
