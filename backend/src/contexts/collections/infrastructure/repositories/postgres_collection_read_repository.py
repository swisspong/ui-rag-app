from typing import Any, List, Tuple
import json
from datetime import timezone

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.collections.domain.value_objects.collection_name import CollectionName
from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.application.queries.repositories.collection_read_repository import CollectionReadRepository
from src.contexts.collections.application.queries.models.collection_read_model import (
    CollectionReadModel,
    LLMConfigReadModel,
    EmbeddingConfigReadModel,
    ChunkingConfigReadModel
)
from src.contexts.collections.application.queries.models.collection_file_read_model import CollectionFileReadModel
from src.contexts.collections.application.queries.get_collection_list.get_collection_list_input import GetCollectionListInput
from src.contexts.collections.infrastructure.sql.exists_by_name_collection import EXISTS_BY_NAME_COLLECTION
from src.contexts.collections.infrastructure.sql.get_collection_list import GET_COLLECTION_LIST
from src.contexts.collections.infrastructure.sql.count_collections import COUNT_COLLECTIONS
from src.contexts.collections.infrastructure.sql.get_files_in_collection import GET_FILES_IN_COLLECTION
from src.shared.infrastructure.errors import QueryFailed, DatabaseError


class PostgresCollectionReadRepository(CollectionReadRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def exists_by_name(self, name: CollectionName, conn: Any = None) -> bool:
        try:
            row = await self._db.fetchrow(
                EXISTS_BY_NAME_COLLECTION,
                name.value,
                conn=conn,
            )
            return row is not None
        except DatabaseError:
            raise
        except Exception as e:
            raise QueryFailed("EXISTS_BY_NAME_COLLECTION", e) from e

    async def get_list(self, input_data: GetCollectionListInput, conn: Any = None) -> List[CollectionReadModel]:
        try:
            rows = await self._db.fetch(
                GET_COLLECTION_LIST,
                input_data.search,
                input_data.order_by,
                input_data.limit,
                input_data.offset,
                conn=conn,
            )

            collections = []
            for row in rows:

                collection = CollectionReadModel(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    file_count=row['file_count'],
                    created_at=row['created_at'].replace(tzinfo=timezone.utc),
                    updated_at=row['updated_at'].replace(tzinfo=timezone.utc)
                )
                collections.append(collection)

            return collections
        except DatabaseError as e:
            raise QueryFailed("GET_COLLECTION_LIST", e) from e

    async def get_list_with_count(self, input_data: GetCollectionListInput, conn: Any = None) -> Tuple[List[CollectionReadModel], int]:
        try:
            # Get the collections
            collections = await self.get_list(input_data, conn)

            # Get the total count
            count_row = await self._db.fetchrow(
                COUNT_COLLECTIONS,
                input_data.search,
                conn=conn,
            )

            total_count = count_row['total_count'] if count_row else 0

            return collections, total_count
        except DatabaseError as e:
            raise QueryFailed("GET_COLLECTION_LIST_WITH_COUNT", e) from e

    async def get_files_in_collection(self, collection_id: CollectionID, conn: Any = None) -> List[CollectionFileReadModel]:
        try:
            rows = await self._db.fetch(
                GET_FILES_IN_COLLECTION,
                collection_id.value,
                conn=conn,
            )

            files = []
            for row in rows:
                file = CollectionFileReadModel(
                    collection_file_id=row['collection_file_id'],
                    filename=row['filename'],
                    size=row['size'],
                    asset_id=row['asset_id'],
                    created_at=row['created_at'],
                    current_stage=row['current_stage'],
                    status=row['status']
                )
                files.append(file)

            return files
        except DatabaseError as e:
            raise QueryFailed("GET_FILES_IN_COLLECTION", e) from e
