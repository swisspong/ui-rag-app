from dataclasses import dataclass
from typing import Optional

from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class GetDocumentsInCollectionInput:
    collection_id: CollectionID
    search: Optional[str] = None
    order_by: str = "created_at"
    limit: int = 10
    offset: int = 0
