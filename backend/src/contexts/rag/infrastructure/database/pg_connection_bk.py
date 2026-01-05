import asyncpg
from contextlib import asynccontextmanager


class AsyncPGConnection:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(dsn=self._dsn, min_size=1, max_size=10)

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def transaction(self):
        """
        ใช้สำหรับ atomic operation เช่นใน use case หรือ repository ที่ต้องการ begin/commit
        """
        if not self._pool:
            raise RuntimeError(
                "Database pool not initialized. Call connect() first.")

        async with self._pool.acquire() as connection:
            async with connection.transaction():
                yield connection

    async def execute(self, query: str, *args):
        """
        Execute SQL (INSERT/UPDATE/DELETE)
        """
        async with self._pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        """
        Fetch หลายแถว (SELECT)
        """
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """
        Fetch แถวเดียว
        """
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
