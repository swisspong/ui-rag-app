from typing import Any, Optional

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.domain.entities.rag_process import RAGProcess
from src.contexts.rag.domain.repositories.rag_process_repository import RAGProcessRepository
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.rag_process_id import RAGProcessID
from src.contexts.rag.domain.value_objects.stage_execution import (
    ProcessStatus,
    ProcessStage,
    StageExecution
)
from src.contexts.rag.infrastructure.sql.save_rag_process import SAVE_RAG_PROCESS
from src.contexts.rag.infrastructure.sql.get_rag_process_by_document_id import GET_RAG_PROCESS_BY_DOCUMENT_ID
from src.contexts.rag.infrastructure.sql.get_rag_process_by_collection_and_file_id import GET_RAG_PROCESS_BY_COLLECTION_AND_FILE_ID
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresRAGProcessRepository(RAGProcessRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: RAGProcess, conn: Any = None) -> RAGProcess:
        try:
            await self._db.execute(
                SAVE_RAG_PROCESS,
                data.id.value,                    # 1. id
                data.collection_id.value,         # 2. collection_id
                data.collection_file_id.value,    # 3. collection_file_id
                data.status.value,                # 4. status
                data.current_stage.value if data.current_stage else None,  # 5. current_stage
                data.ocr.status.value,            # 6. ocr_status
                data.ocr.started_at,              # 7. ocr_started_at
                data.ocr.finished_at,             # 8. ocr_finished_at
                data.ingest.status.value,         # 9. ingest_status
                data.ingest.started_at,           # 10. ingest_started_at
                data.ingest.finished_at,          # 11. ingest_finished_at
                data.chunking.status.value,       # 12. chunking_status
                data.chunking.started_at,         # 13. chunking_started_at
                data.chunking.finished_at,        # 14. chunking_finished_at
                data.error_code,                  # 15. error_code
                data.error_message,               # 16. error_message
                data.document_id.value if data.document_id else None,  # 17. document_id
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise
        except DatabaseError as e:
            print(e)
            raise QueryFailed("SAVE_RAG_PROCESS", e) from e

    async def get_by_document_id_and_collection_id(self, document_id: DocumentID, collection_id: CollectionID, conn: Any = None) -> Optional[RAGProcess]:
        try:
            row = await self._db.fetchrow(
                GET_RAG_PROCESS_BY_DOCUMENT_ID,
                document_id.value,
                collection_id.value,
                conn=conn,
            )
            
            if row is None:
                return None
                
            return RAGProcess(
                id=RAGProcessID.from_value(row['id']),
                collection_id=CollectionID.from_value(row['collection_id']),
                collection_file_id=CollectionFileID.from_value(row['collection_file_id']),
                status=ProcessStatus(row['status']),
                current_stage=ProcessStage(row['current_stage']) if row['current_stage'] else None,
                ocr=StageExecution(
                    status=ProcessStatus(row['ocr_status']),
                    started_at=row['ocr_started_at'],
                    finished_at=row['ocr_finished_at'],
                ),
                ingest=StageExecution(
                    status=ProcessStatus(row['ingest_status']),
                    started_at=row['ingest_started_at'],
                    finished_at=row['ingest_finished_at'],
                ),
                chunking=StageExecution(
                    status=ProcessStatus(row['chunking_status']),
                    started_at=row['chunking_started_at'],
                    finished_at=row['chunking_finished_at'],
                ),
                error_code=row['error_code'],
                error_message=row['error_message'],
                document_id=DocumentID.from_value(row['document_id']) if row['document_id'] else None,
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
            
        except DatabaseError as e:
            print(e)
            raise QueryFailed("GET_RAG_PROCESS_BY_DOCUMENT_ID", e) from e

    async def get_by_collection_id_and_collection_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> Optional[RAGProcess]:
        try:
            row = await self._db.fetchrow(
                GET_RAG_PROCESS_BY_COLLECTION_AND_FILE_ID,
                collection_id.value,
                collection_file_id.value,
                conn=conn,
            )
            
            if row is None:
                return None
                
            return RAGProcess(
                id=RAGProcessID.from_value(row['id']),
                collection_id=CollectionID.from_value(row['collection_id']),
                collection_file_id=CollectionFileID.from_value(row['collection_file_id']),
                status=ProcessStatus(row['status']),
                current_stage=ProcessStage(row['current_stage']) if row['current_stage'] else None,
                ocr=StageExecution(
                    status=ProcessStatus(row['ocr_status']),
                    started_at=row['ocr_started_at'],
                    finished_at=row['ocr_finished_at'],
                ),
                ingest=StageExecution(
                    status=ProcessStatus(row['ingest_status']),
                    started_at=row['ingest_started_at'],
                    finished_at=row['ingest_finished_at'],
                ),
                chunking=StageExecution(
                    status=ProcessStatus(row['chunking_status']),
                    started_at=row['chunking_started_at'],
                    finished_at=row['chunking_finished_at'],
                ),
                error_code=row['error_code'],
                error_message=row['error_message'],
                document_id=DocumentID.from_value(row['document_id']) if row['document_id'] else None,
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
            
        except DatabaseError as e:
            print(e)
            raise QueryFailed("GET_RAG_PROCESS_BY_COLLECTION_AND_FILE_ID", e) from e
