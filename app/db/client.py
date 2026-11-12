import logging
from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

log = logging.getLogger(__name__)


class Database:
    """psycopg 3 pool үшін жұқа орауыш.

    - Сұраныстарда %s placeholder қолданылады.
    - prepare_threshold=None: Supabase pooler (transaction mode, 6543) prepared statement қолдамайды.
    - autocommit: әр сұраныс жеке транзакция; бірнеше сұранысты біріктіру үшін transaction() қолданыңыз.
    """

    def __init__(self) -> None:
        self._pool: AsyncConnectionPool | None = None

    @property
    def pool(self) -> AsyncConnectionPool:
        if self._pool is None:
            raise RuntimeError("Database әлі қосылмаған. connect() шақырыңыз.")
        return self._pool

    async def connect(self, dsn: str, min_size: int = 1, max_size: int = 5) -> None:
        self._pool = AsyncConnectionPool(
            conninfo=dsn,
            min_size=min_size,
            max_size=max_size,
            kwargs={"autocommit": True, "row_factory": dict_row, "prepare_threshold": None},
            open=False,
        )
        await self._pool.open()
        await self._pool.wait(timeout=30)
        log.info("Деректер базасына қосылды")

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        async with self.pool.connection() as conn:
            cur = await conn.execute(query, args or None)
            return await cur.fetchall()

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        async with self.pool.connection() as conn:
            cur = await conn.execute(query, args or None)
            return await cur.fetchone()

    async def fetchval(self, query: str, *args: Any) -> Any:
        row = await self.fetchrow(query, *args)
        return next(iter(row.values())) if row else None

    async def execute(self, query: str, *args: Any) -> None:
        async with self.pool.connection() as conn:
            await conn.execute(query, args or None)
