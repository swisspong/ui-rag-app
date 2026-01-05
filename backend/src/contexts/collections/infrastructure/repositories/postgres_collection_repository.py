from typing import Any
import json

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.collections.domain.entities.collection import Collection
from src.contexts.collections.domain.repositories.collection_repository import CollectionRepository
from src.contexts.collections.infrastructure.sql.save_collection import SAVE_COLLECTION
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresCollectionRepository(CollectionRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: Collection, conn: Any = None) -> Collection:
        try:
            await self._db.execute(
                SAVE_COLLECTION,
                data.id.value,
                data.name.value,
                data.description.value,
                data.created_at,
                data.updated_at,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise 
        except DatabaseError as e:
            raise QueryFailed("SAVE_COLLECTION", e) from e
