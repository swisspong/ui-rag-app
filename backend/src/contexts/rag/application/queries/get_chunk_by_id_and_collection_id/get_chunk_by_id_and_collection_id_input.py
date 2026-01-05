from dataclasses import dataclass
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class GetChunkByIdAndCollectionIdInput:
    chunk_id: ChunkID
    collection_id: CollectionID
