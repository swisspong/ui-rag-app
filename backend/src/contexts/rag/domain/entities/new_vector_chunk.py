from typing import List, Dict, Any
import time
from dataclasses import dataclass

from src.contexts.rag.domain.value_objects.vector_chunk_id import VectorChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID


@dataclass
class NewVectorChunk:

    id: VectorChunkID
    chunk_id: ChunkID
    collection_id: CollectionID
    vector: List[float]
    content: str
    meta: Dict[str, Any]
    created_at: int

    @staticmethod
    def create(
        id: VectorChunkID,
        chunk_id: ChunkID,
        collection_id: CollectionID,
        vector: List[float],
        content: str,
        meta: Dict[str, Any],
    ) -> "NewVectorChunk":
        # now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)
        now = int(time.time())
        return NewVectorChunk(
            id=id,
            chunk_id=chunk_id,
            collection_id=collection_id,
            vector=vector,
            content=content,
            meta=meta,
            created_at=now
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id.value,
            "chunk_id": self.chunk_id.value,
            "collection_id": self.collection_id.value,
            "vector": self.vector,
            "content": self.content,
            "meta": self.meta,
            "created_at": self.created_at,
        }
