from dataclasses import dataclass
import datetime
from datetime import timezone

from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.document_name import DocumentName
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.shared.domain.value_objects.asset_id import AssetID


@dataclass
class Document:
    id: DocumentID
    name: DocumentName
    collection_id: CollectionID
    collection_file_id: CollectionFileID
    content: str
    asset_id: AssetID
    status: ProcessStatus
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: DocumentID,
        name: DocumentName,
        collection_id: CollectionID,
        collection_file_id: CollectionFileID,
        content: str,
        asset_id: AssetID,
        status: ProcessStatus = ProcessStatus.PENDING
    ) -> "Document":

        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return Document(
            id=id,
            name=name,
            collection_id=collection_id,
            collection_file_id=collection_file_id,
            content=content,
            asset_id=asset_id,
            status=status,
            created_at=now,
            updated_at=now
        )

    def mark_as_running(self) -> None:
        self.status = ProcessStatus.RUNNING
        self.updated_at = datetime.datetime.now(
            timezone.utc).replace(tzinfo=None)

    def mark_as_completed(self, content: str) -> None:
        self.status = ProcessStatus.COMPLETED
        self.content = content
        self.updated_at = datetime.datetime.now(
            timezone.utc).replace(tzinfo=None)

    def mark_as_failed(self) -> None:
        self.status = ProcessStatus.FAILED
        self.updated_at = datetime.datetime.now(
            timezone.utc).replace(tzinfo=None)
