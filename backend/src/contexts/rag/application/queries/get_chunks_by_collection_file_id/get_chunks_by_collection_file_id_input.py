from dataclasses import dataclass
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID


@dataclass
class GetChunksByCollectionFileIdInput:
    collection_id: CollectionID
    collection_file_id: CollectionFileID
