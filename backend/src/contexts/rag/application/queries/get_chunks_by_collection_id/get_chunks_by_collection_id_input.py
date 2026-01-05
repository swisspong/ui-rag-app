from dataclasses import dataclass
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class GetChunksByCollectionIdInput:
    collection_id: CollectionID
