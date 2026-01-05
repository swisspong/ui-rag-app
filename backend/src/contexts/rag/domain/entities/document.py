from dataclasses import dataclass
import datetime
from datetime import timezone

from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.shared.domain.value_objects.asset_id import AssetID


@dataclass
class Document:
    id: DocumentID
    collection_id: CollectionID
    collection_file_id: CollectionFileID
    content: str
    asset_id: AssetID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: DocumentID,
        collection_id: CollectionID,
        collection_file_id: CollectionFileID,
        content: str,
        asset_id: AssetID
    ) -> "Document":

        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return Document(
            id=id,
            collection_id=collection_id,
            collection_file_id=collection_file_id,
            content=content,
            asset_id=asset_id,
            created_at=now,
            updated_at=now
        )
