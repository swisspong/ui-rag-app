from dataclasses import dataclass
from typing import List

from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class DeleteMultipleChunksInput:
    collection_id: CollectionID
    chunk_ids: List[ChunkID]
