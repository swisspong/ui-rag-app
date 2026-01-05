from typing import Any, List, Optional
import json

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.domain.entities.new_chunk import Chunk
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.contexts.rag.infrastructure.sql.save_chunk import SAVE_CHUNK
from src.contexts.rag.infrastructure.sql.get_chunks_by_collection_id import GET_CHUNKS_BY_COLLECTION_ID
from src.contexts.rag.infrastructure.sql.get_chunk_by_id_and_collection_id import GET_CHUNK_BY_ID_AND_COLLECTION_ID
from src.contexts.rag.infrastructure.sql.delete_chunk_by_id_and_collection_id import DELETE_CHUNK_BY_ID_AND_COLLECTION_ID
from src.contexts.rag.infrastructure.sql.delete_multiple_chunks_by_ids_and_collection_id import DELETE_MULTIPLE_CHUNKS_BY_IDS_AND_COLLECTION_ID
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresChunkRepository(ChunkRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: Chunk, conn: Any = None) -> Chunk:
        try:
            await self._db.execute(
                SAVE_CHUNK,
                data.id.value,
                data.document_id.value,
                data.collection_id.value,
                data.content,
                data.order_index,
                json.dumps(data.meta),
                data.process_status.value,
                data.created_at,
                data.updated_at,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise
        except DatabaseError as e:
            print(e)
            raise QueryFailed("SAVE_CHUNK", e) from e

    async def get_by_document_id_in_collection(self, collection_id: CollectionID, document_id: DocumentID, conn: Any = None) -> List[Chunk]:
        try:
            rows = await self._db.fetch(
                GET_CHUNKS_BY_COLLECTION_ID,
                collection_id.value,
                document_id.value,
                conn=conn
            )
            return [
                Chunk(
                    id=ChunkID.from_value(row["id"]),
                    document_id=document_id,
                    collection_id=collection_id,
                    content=row["content"],
                    order_index=row["order_index"],
                    meta=json.loads(row["meta"]) if row["meta"] else {},
                    process_status=ProcessStatus(row["process_status"]) if row.get("process_status") else ProcessStatus.PENDING,
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                for row in rows
            ]
        except DatabaseError as e:
            raise QueryFailed("GET_CHUNKS_BY_COLLECTION_ID", e) from e

    async def get_by_id_and_collection_id(self, chunk_id: ChunkID, collection_id: CollectionID, conn: Any = None) -> Optional[Chunk]:
        try:
            row = await self._db.fetchrow(
                GET_CHUNK_BY_ID_AND_COLLECTION_ID,
                chunk_id.value,
                collection_id.value,
                conn=conn
            )

            if row is None:
                return None

            return Chunk(
                id=ChunkID.from_value(row["id"]),
                document_id=DocumentID.from_value(row["document_id"]),
                collection_id=CollectionID.from_value(row["collection_id"]),
                content=row["content"],
                order_index=row["order_index"],
                meta=json.loads(row["meta"]) if row["meta"] else {},
                process_status=ProcessStatus(row["process_status"]) if row.get("process_status") else ProcessStatus.PENDING,
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        except DatabaseError as e:
            raise QueryFailed("GET_CHUNK_BY_ID_AND_COLLECTION_ID", e) from e

    async def delete_by_id_and_collection_id(self, chunk_id: ChunkID, collection_id: CollectionID, conn: Any = None) -> bool:
        try:
            result = await self._db.execute(
                DELETE_CHUNK_BY_ID_AND_COLLECTION_ID,
                chunk_id.value,
                collection_id.value,
                conn=conn
            )
            return result == "DELETE 1"
        except DatabaseError as e:
            raise QueryFailed("DELETE_CHUNK_BY_ID_AND_COLLECTION_ID", e) from e

    async def delete_multiple_by_ids_and_collection_id(self, chunk_ids: List[ChunkID], collection_id: CollectionID, conn: Any = None) -> int:
        try:
            if not chunk_ids:
                return 0
            
            chunk_id_values = [chunk_id.value for chunk_id in chunk_ids]
            result = await self._db.execute(
                DELETE_MULTIPLE_CHUNKS_BY_IDS_AND_COLLECTION_ID,
                chunk_id_values,
                collection_id.value,
                conn=conn
            )
            # Parse result to get the number of deleted rows
            # result format is "DELETE <count>"
            deleted_count = int(result.split()[1]) if result and result.startswith("DELETE") else 0
            return deleted_count
        except DatabaseError as e:
            raise QueryFailed("DELETE_MULTIPLE_CHUNKS_BY_IDS_AND_COLLECTION_ID", e) from e
