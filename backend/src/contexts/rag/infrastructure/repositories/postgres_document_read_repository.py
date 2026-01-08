from typing import Any, List, Optional

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.application.queries.models.document_read_model import DocumentReadModel
from src.contexts.rag.application.queries.repoistories.document_read_repository import DocumentReadRepository
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.infrastructure.sql.get_documents_in_collection import GET_DOCUMENTS_IN_COLLECTION
from src.contexts.rag.infrastructure.sql.count_documents_in_collection import COUNT_DOCUMENTS_IN_COLLECTION
from src.contexts.rag.infrastructure.sql.get_document_by_collection_and_file_id import GET_DOCUMENT_BY_COLLECTION_AND_FILE_ID
from src.shared.infrastructure.errors import (
    QueryFailed,
    DatabaseError
)


class PostgresDocumentReadRepository(DocumentReadRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def get_by_collection_id(
        self,
        collection_id: CollectionID,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
        conn: Any = None
    ) -> List[DocumentReadModel]:
        try:
            rows = await self._db.fetch(
                GET_DOCUMENTS_IN_COLLECTION,
                collection_id.value,
                search,
                limit,
                offset,
                conn=conn,
            )

            return [
                DocumentReadModel(
                    id=row['id'],
                    collection_file_id=row['collection_file_id'],
                    name=row['name'],
                    filename=row['filename'],
                    status=row['status'],
                    content=row['content'],
                    created_at=row['created_at']
                )
                for row in rows
            ]

        except DatabaseError as e:
            print(e)
            raise QueryFailed("GET_DOCUMENTS_IN_COLLECTION", e) from e

    async def get_by_collection_and_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> Optional[DocumentReadModel]:
        try:
            row = await self._db.fetchrow(
                GET_DOCUMENT_BY_COLLECTION_AND_FILE_ID,
                collection_id.value,
                collection_file_id.value,
                conn=conn,
            )

            if row is None:
                return None

            return DocumentReadModel(
                id=row['id'],
                collection_file_id=row['collection_file_id'],
                name=row['name'],
                filename=row['filename'],
                status=row['status'],
                content=row['content'],
                created_at=row['created_at']
            )
        except DatabaseError as e:
            print(e)
            raise QueryFailed(
                "GET_DOCUMENT_BY_COLLECTION_AND_FILE_ID", e) from e

    async def count_by_collection_id(
        self,
        collection_id: CollectionID,
        search: Optional[str] = None,
        conn: Any = None
    ) -> int:
        try:
            row = await self._db.fetchrow(
                COUNT_DOCUMENTS_IN_COLLECTION,
                collection_id.value,
                search,
                conn=conn,
            )
            return row['count']
        except DatabaseError as e:
            print(e)
            raise QueryFailed("COUNT_DOCUMENTS_IN_COLLECTION", e) from e
