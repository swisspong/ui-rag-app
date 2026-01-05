import asyncpg
from contextlib import asynccontextmanager
from typing import Optional
from src.shared.infrastructure.errors import (
    DatabaseError,
    DuplicateRecordError,
    InfrastructureError
)


class AsyncPGConnection:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self._dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None
        self._min_size = min_size
        self._max_size = max_size

    async def connect(self) -> None:
        if self._pool:
            return

        try:
            self._pool = await asyncpg.create_pool(
                dsn=self._dsn,
                min_size=self._min_size,
                max_size=self._max_size,
            )
        except Exception as e:
            raise InfrastructureError("Failed to connect to database") from e

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    def _ensure_connected(self):
        if not self._pool:
            raise InfrastructureError("Database not connected")

    @asynccontextmanager
    async def transaction(self):
        self._ensure_connected()

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def execute(self, query: str, *args, conn=None) -> str:
        self._ensure_connected()

        try:
            if conn:
                return await conn.execute(query, *args)
            else:
                async with self._pool.acquire() as conn:
                    return await conn.execute(query, *args)

        except asyncpg.UniqueViolationError as e:
            print(e)
            raise DuplicateRecordError("Duplicate Record") from e
        except asyncpg.PostgresError as e:
            print(e)
            raise DatabaseError("Database execution error") from e

    async def fetch(self, query: str, *args, conn=None):
        self._ensure_connected()

        try:
            if conn:
                return await conn.fetch(query, *args)

            async with self._pool.acquire() as conn:
                return await conn.fetch(query, *args)

        except asyncpg.PostgresError as e:
            print(e)
            raise DatabaseError("Database fetch error") from e

    async def fetchrow(self, query: str, *args, conn=None):
        self._ensure_connected()

        try:
            if conn:
                return await conn.fetchrow(query, *args)

            async with self._pool.acquire() as conn:
                return await conn.fetchrow(query, *args)

        except asyncpg.PostgresError as e:
            print(e)
            raise DatabaseError("Database fetchrow error") from e
