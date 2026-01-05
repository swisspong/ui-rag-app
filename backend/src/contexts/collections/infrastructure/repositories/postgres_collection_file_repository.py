from typing import Any

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.collections.domain.entities.collection_file import CollectionFile
from src.contexts.collections.domain.repositories.collection_file_repository import CollectionFileRepository
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID
from src.shared.domain.value_objects.asset_id import AssetID
from src.contexts.collections.infrastructure.sql.save_collection_file import SAVE_COLLECTION_FILE
from src.contexts.collections.infrastructure.sql.get_collection_file_many_by_collection_id import GET_COLLECTION_FILE_MANY_BY_COLLECTION_ID
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresCollectionFileRepository(CollectionFileRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: CollectionFile, conn: Any = None) -> CollectionFile:
        try:
            await self._db.execute(
                SAVE_COLLECTION_FILE,
                data.id.value,
                data.collection_id.value,
                data.asset_id.value,
                data.created_at,
                data.updated_at,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise 
        except DatabaseError as e:
            raise QueryFailed("SAVE_COLLECTION_FILE", e) from e

    async def get_many_by_collection_id(self, data, conn: Any = None) -> list[CollectionFile]:
        try:
            rows = await self._db.fetch(
                GET_COLLECTION_FILE_MANY_BY_COLLECTION_ID,
                data.value,
                conn=conn,
            )
            return [
                CollectionFile(
                    id=CollectionFileID.from_value(row["id"]),
                    collection_id=data,
                    asset_id=AssetID.from_value(row["asset_id"]),
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                for row in rows
            ]
        except DatabaseError as e:
            raise QueryFailed("GET_COLLECTION_FILE_MANY_BY_COLLECTION_ID", e) from e
