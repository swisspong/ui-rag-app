from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


@dataclass
class UpdateChunkInput:
    collection_id: CollectionID
    chunk_id: ChunkID
    content: str
    meta: Optional[Dict[str, Any]] = None
