from .asyncpg_connection import AsyncPGConnection


class UnitOfWork:
    def __init__(self, db: AsyncPGConnection):
        self._db = db
        self.conn = None

    async def __aenter__(self):
        self._ctx = self._db.transaction()
        self.conn = await self._ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._ctx.__aexit__(exc_type, exc, tb)
