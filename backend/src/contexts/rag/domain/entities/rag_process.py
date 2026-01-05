from dataclasses import dataclass
from typing import Optional
import datetime
from datetime import timezone

from src.contexts.rag.domain.value_objects.rag_process_id import RAGProcessID
from src.contexts.rag.domain.value_objects.stage_execution import (
    ProcessStage,
    ProcessStatus,
    StageExecution
)
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.shared.domain.errors import DomainError


@dataclass
class RAGProcess:
    id: RAGProcessID
    collection_id: CollectionID
    collection_file_id: CollectionFileID
    status: ProcessStatus
    current_stage: Optional[ProcessStage]
    ocr: StageExecution
    chunking: StageExecution
    ingest: StageExecution
    error_code: Optional[str]
    error_message: Optional[str]
    document_id: Optional[DocumentID]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: RAGProcessID,
        collection_id: CollectionID,
        collection_file_id: CollectionFileID,
    ) -> "RAGProcess":
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        return RAGProcess(
            id=id,
            collection_id=collection_id,
            collection_file_id=collection_file_id,
            status=ProcessStatus.PENDING,
            current_stage=ProcessStage.OCR,
            ocr=StageExecution.pending(),
            chunking=StageExecution.pending(),
            ingest=StageExecution.pending(),
            error_code=None,
            error_message=None,
            document_id=None,
            created_at=now,
            updated_at=now,
        )

    def start_ocr(self):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        if self.status not in [ProcessStatus.PENDING]:
            raise DomainError("Cannot start OCR")

        self.status = ProcessStatus.RUNNING
        self.current_stage = ProcessStage.OCR
        self.ocr = self.ocr.start(now)
        self.updated_at = now

    def finish_ocr(self, document_id: DocumentID):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        if self.current_stage != ProcessStage.OCR:
            raise DomainError("OCR not running")
        self.status = ProcessStatus.COMPLETED
        self.ocr = self.ocr.finish(now)
        self.document_id = document_id
        # self.current_stage = None
        self.updated_at = now

    def start_chunking(self):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        # if self.status not in [ProcessStatus.PENDING, ProcessStatus.RUNNING]:
        if self.status not in [ProcessStatus.COMPLETED] and self.current_stage not in [ProcessStage.OCR]:
            print("in domain error")
            raise DomainError("Cannot start chunking")

        self.status = ProcessStatus.RUNNING
        self.current_stage = ProcessStage.CHUNKING
        self.chunking = self.chunking.start(now)
        self.updated_at = now

    def finish_chunking(self):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        if self.current_stage != ProcessStage.CHUNKING:
            raise DomainError("Chunking not running")

        self.status = ProcessStatus.COMPLETED
        self.chunking = self.chunking.finish(now)
        # self.current_stage = None
        self.updated_at = now

    def start_ingest(self):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        if self.ocr.status != ProcessStatus.COMPLETED or self.chunking.status != ProcessStatus.COMPLETED:
            raise DomainError("OCR and chunking not completed")

        self.current_stage = ProcessStage.INGEST
        self.ingest = self.ingest.start(now)
        self.updated_at = now

    def finish_ingest(self):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        if self.current_stage != ProcessStage.INGEST:
            raise DomainError("Ingest not running")

        self.ingest = self.ingest.finish(now)
        self.status = ProcessStatus.COMPLETED
        # self.current_stage = None
        self.updated_at = now
