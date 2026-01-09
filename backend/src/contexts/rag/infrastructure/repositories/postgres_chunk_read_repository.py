from typing import Any, List, Optional
import json
from datetime import timezone

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.application.queries.models.document_chunk_summary_read_model import DocumentChunkSummaryReadModel
from src.contexts.rag.application.queries.models.document_chunk_read_model import DocumentChunkReadModel
from src.contexts.rag.infrastructure.sql.get_chunks_by_collection_and_file_id import GET_CHUNKS_BY_COLLECTION_AND_FILE_ID
from src.contexts.rag.infrastructure.sql.get_chunk_by_id_and_collection_id import GET_CHUNK_BY_ID_AND_COLLECTION_ID
from src.contexts.rag.infrastructure.sql.get_all_chunks_by_collection_id import GET_ALL_CHUNKS_BY_COLLECTION_ID
from src.contexts.rag.infrastructure.sql.get_document_summaries_in_collection import (
    GET_DOCUMENT_SUMMARIES_IN_COLLECTION,
    COUNT_DOCUMENT_SUMMARIES_IN_COLLECTION
)
from src.contexts.rag.infrastructure.sql.get_chunks_by_collection_file_id_with_pagination import (
    GET_CHUNKS_WITH_PAGINATION,
    COUNT_CHUNKS
)
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID
from src.shared.infrastructure.errors import (
    QueryFailed,
    DatabaseError
)


class PostgresChunkReadRepository(ChunkReadRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def get_by_collection_and_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> List[ChunkReadModel]:
        try:
            rows = await self._db.fetch(
                GET_CHUNKS_BY_COLLECTION_AND_FILE_ID,
                collection_id.value,
                collection_file_id.value,
                conn=conn,
            )

            return [
                ChunkReadModel(
                    id=row['id'],
                    collection_id=row['collection_id'],
                    document_id=row['document_id'],
                    content=row['content'],
                    meta=json.loads(row['meta']) if row['meta'] else {},
                    order_index=row['order_index'],
                    process_status=row['process_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_CHUNKS_BY_COLLECTION_AND_FILE_ID", e) from e

    async def get_by_id_and_collection_id(self, chunk_id: str, collection_id: str, conn: Any = None) -> Optional[ChunkReadModel]:
        try:
            row = await self._db.fetchrow(
                GET_CHUNK_BY_ID_AND_COLLECTION_ID,
                chunk_id,
                collection_id,
                conn=conn,
            )

            if row is None:
                return None

            return ChunkReadModel(
                id=row['id'],
                collection_id=row['collection_id'],
                document_id=row['document_id'],
                content=row['content'],
                meta=json.loads(row['meta']) if row['meta'] else {},
                order_index=row['order_index'],
                process_status=row['process_status'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )

        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_CHUNK_BY_ID_AND_COLLECTION_ID", e) from e

    async def get_by_collection_id(self, collection_id: CollectionID, conn: Any = None) -> List[ChunkReadModel]:
        try:
            rows = await self._db.fetch(
                GET_ALL_CHUNKS_BY_COLLECTION_ID,
                collection_id.value,
                conn=conn,
            )

            return [
                ChunkReadModel(
                    id=row['id'],
                    collection_id=row['collection_id'],
                    document_id=row['document_id'],
                    content=row['content'],
                    meta=json.loads(row['meta']) if row['meta'] else {},
                    order_index=row['order_index'],
                    process_status=row['process_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_ALL_CHUNKS_BY_COLLECTION_ID", e) from e

    async def get_document_summaries_by_collection_id(
        self,
        collection_id: CollectionID,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        conn: Any = None
    ) -> tuple[List[DocumentChunkSummaryReadModel], int]:
        try:
            search_param = f"%{search}%" if search else None

            # Get total count
            count_row = await self._db.fetchrow(
                COUNT_DOCUMENT_SUMMARIES_IN_COLLECTION,
                collection_id.value,
                search_param,
                conn=conn
            )
            total = count_row['total'] if count_row else 0

            # Get data
            rows = await self._db.fetch(
                GET_DOCUMENT_SUMMARIES_IN_COLLECTION,
                collection_id.value,
                search_param,
                offset,
                limit,
                conn=conn
            )

            return [
                DocumentChunkSummaryReadModel(
                    id=row['id'],
                    version=row['version'],
                    name=row['name'],
                    chunk_count=row['chunk_count'],
                    created_at=row['created_at'].replace(tzinfo=timezone.utc)
                )
                for row in rows
            ], total

        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_DOCUMENT_SUMMARIES_IN_COLLECTION", e) from e

    async def get_chunks_by_collection_file_id(
        self,
        collection_id: str,
        document_id: str,
        version: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        conn: Any = None
    ) -> tuple[List[DocumentChunkReadModel], int]:
        try:
            search_param = f"%{search}%" if search else None

            # Get total count
            count_row = await self._db.fetchrow(
                COUNT_CHUNKS,
                collection_id,
                document_id,
                version,
                search_param,
                conn=conn
            )
            total = count_row['total'] if count_row else 0

            # Get data
            rows = await self._db.fetch(
                GET_CHUNKS_WITH_PAGINATION,
                collection_id,
                document_id,
                version,
                search_param,
                offset,
                limit,
                conn=conn
            )

            return [
                DocumentChunkReadModel(
                    id=row['id'],
                    content=row['content'],
                    meta=json.loads(row['meta']) if row['meta'] else {},
                    status=row['status']
                )
                for row in rows
            ], total

        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_CHUNKS_WITH_PAGINATION", e) from e

