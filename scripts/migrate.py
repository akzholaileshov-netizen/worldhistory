"""migrations/*.sql файлдарын тәртіппен қолданады. Іске қосу: python -m scripts.migrate"""

import asyncio
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from app.config import get_settings
from app.core.loop import configure_event_loop

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


async def run() -> None:
    settings = get_settings()
    async with await psycopg.AsyncConnection.connect(
        settings.database_url.get_secret_value(),
        autocommit=True,
        row_factory=dict_row,
        prepare_threshold=None,
    ) as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
        )
        cur = await conn.execute("SELECT name FROM schema_migrations")
        applied = {r["name"] for r in await cur.fetchall()}

        pending = [f for f in sorted(MIGRATIONS_DIR.glob("*.sql")) if f.name not in applied]
        if not pending:
            print("Жаңа миграция жоқ. Барлығы өзекті.")
            return

        for f in pending:
            print(f"-> {f.name} қолданылуда...")
            sql = f.read_text(encoding="utf-8")
            async with conn.transaction():
                await conn.execute(sql)
                await conn.execute("INSERT INTO schema_migrations (name) VALUES (%s)", (f.name,))
            print(f"   OK {f.name}")
        print("Дайын.")


if __name__ == "__main__":
    configure_event_loop()
    asyncio.run(run())
