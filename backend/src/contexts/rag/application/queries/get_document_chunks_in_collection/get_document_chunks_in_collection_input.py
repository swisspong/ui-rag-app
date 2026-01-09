from dataclasses import dataclass
from typing import Optional
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class GetDocumentChunksInCollectionInput:
    collection_id: CollectionID
    offset: int = 0
    limit: int = 10
    search: Optional[str] = None
