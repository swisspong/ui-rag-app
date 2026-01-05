# shared/infra/db/asyncpg_connection.py

import asyncpg
from contextlib import asynccontextmanager
from typing import Optional
from .errors import DuplicateKeyError, DatabaseError


class AsyncPGConnection:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self._dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None
        self._min_size = min_size
        self._max_size = max_size

    async def connect(self) -> None:
        if self._pool:
            return

        self._pool = await asyncpg.create_pool(
            dsn=self._dsn,
            min_size=self._min_size,
            max_size=self._max_size,
        )

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    def _ensure_connected(self):
        if not self._pool:
            raise RuntimeError("Database not connected")

    @asynccontextmanager
    async def transaction(self):
        """
        Application layer เป็นคนควบคุม transaction
        """
        self._ensure_connected()

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def execute(self, query: str, *args, conn=None) -> None:
        """
        ใช้ได้ทั้งในและนอก transaction
        """
        self._ensure_connected()

        try:
            if conn:
                await conn.execute(query, *args)
            else:
                async with self._pool.acquire() as conn:
                    await conn.execute(query, *args)

        except asyncpg.UniqueViolationError as e:
            raise DuplicateKeyError(str(e)) from e
        except asyncpg.PostgresError as e:
            raise DatabaseError(str(e)) from e

    async def fetch(self, query: str, *args, conn=None):
        self._ensure_connected()

        try:
            if conn:
                return await conn.fetch(query, *args)

            async with self._pool.acquire() as conn:
                return await conn.fetch(query, *args)

        except asyncpg.PostgresError as e:
            raise DatabaseError(str(e)) from e

    async def fetchrow(self, query: str, *args, conn=None):
        self._ensure_connected()

        try:
            if conn:
                return await conn.fetchrow(query, *args)

            async with self._pool.acquire() as conn:
                return await conn.fetchrow(query, *args)

        except asyncpg.PostgresError as e:
            raise DatabaseError(str(e)) from e
