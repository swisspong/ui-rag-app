import datetime
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import timezone

from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.contexts.rag.domain.errors.chunk_ingest_not_allowed import ChunkIngestNotAllowed


@dataclass
class Chunk:
    id: ChunkID
    document_id: DocumentID
    collection_id: CollectionID
    content: str
    order_index: int
    meta: Dict[str, Any]
    process_status: ProcessStatus
    created_at: datetime
    updated_at: datetime
    version: int = 1

    @staticmethod
    def create(
        id: ChunkID,
        document_id: DocumentID,
        collection_id: CollectionID,
        content: str,
        order_index: int,
        meta:  Dict[str, Any],
        process_status: ProcessStatus = ProcessStatus.PENDING,
        version: int = 1
    ):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return Chunk(
            id=id,
            document_id=document_id,
            collection_id=collection_id,
            content=content,
            order_index=order_index,
            meta=meta,
            process_status=process_status,
            version=version,
            created_at=now,
            updated_at=now,
        )

    def update(self, content: str, meta: Optional[Dict[str, Any]] = None, process_status: Optional[ProcessStatus] = None) -> None:
        """Update chunk content, metadata, and process status."""
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        self.content = content
        if meta is not None:
            self.meta = meta
        if process_status is not None:
            self.process_status = process_status

        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        self.updated_at = now

    def start_processing(self) -> None:
        """Mark the chunk as currently being processed."""
        self.process_status = ProcessStatus.RUNNING
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        self.updated_at = now

    def complete_processing(self) -> None:
        """Mark the chunk as successfully processed."""
        self.process_status = ProcessStatus.COMPLETED
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        self.updated_at = now

    def fail_processing(self) -> None:
        """Mark the chunk as failed during processing."""
        self.process_status = ProcessStatus.FAILED
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        self.updated_at = now

    def ensure_can_ingest(self) -> None:
        """Check if the chunk can be ingested. Raises ChunkIngestNotAllowed if process status is RUNNING or COMPLETED."""
        if self.process_status in (ProcessStatus.RUNNING, ProcessStatus.COMPLETED):
            raise ChunkIngestNotAllowed(
                process_status=str(self.process_status))
