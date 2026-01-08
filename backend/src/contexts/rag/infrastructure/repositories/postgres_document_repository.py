from typing import Any, Optional

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.domain.entities.document import Document
from src.contexts.rag.domain.repositories.document_repository import DocumentRepository
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.document_name import DocumentName
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.shared.domain.value_objects.asset_id import AssetID
from src.contexts.rag.infrastructure.sql.save_document import SAVE_DOCUMENT
from src.contexts.rag.infrastructure.sql.get_document_by_id import GET_DOCUMENT_BY_ID
from src.contexts.rag.infrastructure.sql.get_documents_by_collection_id import GET_DOCUMENTS_BY_COLLECTION_ID
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresDocumentRepository(DocumentRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: Document, conn: Any = None) -> Document:
        try:
            await self._db.execute(
                SAVE_DOCUMENT,
                data.id.value,
                data.name.value,
                data.collection_id.value,
                data.collection_file_id.value,
                data.content,
                data.asset_id.value,
                data.status.value,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise
        except DatabaseError as e:
            print(e)
            raise QueryFailed("SAVE_DOCUMENT", e) from e

    async def get_by_id(self, document_id: DocumentID, conn: Any = None) -> Optional[Document]:
        try:
            row = await self._db.fetchrow(
                GET_DOCUMENT_BY_ID,
                document_id.value,
                conn=conn,
            )

            if row is None:
                return None

            return Document.create(
                id=DocumentID.from_value(row['id']),
                name=DocumentName.from_value(row['name']),
                collection_id=CollectionID.from_value(row['collection_id']),
                collection_file_id=CollectionFileID.from_value(
                    row['collection_file_id']),
                content=row['content'],
                asset_id=AssetID.from_value(row['asset_id']),
                status=ProcessStatus(row['status'])
            )

        except DatabaseError as e:
            print(e)
            raise QueryFailed("GET_DOCUMENT_BY_ID", e) from e

    async def get_many_by_collection_id(self, collection_id: CollectionID, conn: Any = None) -> list[Document]:
        try:
            rows = await self._db.fetch(
                GET_DOCUMENTS_BY_COLLECTION_ID,
                collection_id.value,
                conn=conn,
            )

            return [
                Document.create(
                    id=DocumentID.from_value(row['id']),
                    name=DocumentName.from_value(row['name']),
                    collection_id=CollectionID.from_value(
                        row['collection_id']),
                    collection_file_id=CollectionFileID.from_value(
                        row['collection_file_id']),
                    content=row['content'],
                    asset_id=AssetID.from_value(row['asset_id']),
                    status=ProcessStatus(row['status'])
                )
                for row in rows
            ]

        except DatabaseError as e:
            print(e)
            raise QueryFailed("GET_DOCUMENTS_BY_COLLECTION_ID", e) from e
