from typing import Literal
from dataclasses import dataclass

from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus


@dataclass(frozen=True)
class EmbedByDocumentInCollectionInput:
    collection_id: CollectionID
    document_id: DocumentID
    version: int
    status: ProcessStatus
