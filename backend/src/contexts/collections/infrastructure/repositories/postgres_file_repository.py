from typing import Any

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.collections.domain.entities.file import File
from src.contexts.collections.domain.repositories.collection_repository import CollectionRepository
from src.contexts.collections.infrastructure.sql.save_file import SAVE_FILE
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresFileRepository(CollectionRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: File, conn: Any = None) -> File:
        try:
            await self._db.execute(
                SAVE_FILE,
                data.id.value,
                data.collection_id.value,
                data.filename,
                data.content_type,
                data.size,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise
        except DatabaseError as e:
            print(e)
            raise QueryFailed("SAVE_COLLECTION", e) from e
