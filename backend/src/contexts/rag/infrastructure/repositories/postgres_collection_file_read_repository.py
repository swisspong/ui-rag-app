from typing import Any, Optional

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.application.queries.repoistories.collection_file_read_repository import CollectionFileReadRepository
from src.contexts.rag.application.queries.models.collection_file_read_model import CollectionFileReadModel
from src.contexts.rag.infrastructure.sql.get_collection_file_in_collection import GET_COLLECTION_FILE_IN_COLLECTION
from src.shared.infrastructure.errors import QueryFailed, DatabaseError


class PostgresCollectionFileReadRepository(CollectionFileReadRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def get_by_collection_and_file_id(self, collection_id: str, collection_file_id: str, conn: Any = None) -> Optional[CollectionFileReadModel]:
        try:
            row = await self._db.fetchrow(
                GET_COLLECTION_FILE_IN_COLLECTION,
                collection_id,
                collection_file_id,
                conn=conn,
            )
            
            if row is None:
                return None
            
            return CollectionFileReadModel(
                id=row['id'],
                collection_id=row['collection_id'],
                asset_id=row['asset_id'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except DatabaseError:
            raise
        except Exception as e:
            raise QueryFailed("GET_COLLECTION_FILE_IN_COLLECTION", e) from e
