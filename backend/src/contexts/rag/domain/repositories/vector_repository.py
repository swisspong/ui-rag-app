from abc import ABC, abstractmethod
from typing import List, Optional
from src.contexts.rag.domain.entities.new_vector_chunk import NewVectorChunk


class VectorRepository(ABC):
    @abstractmethod
    async def saves(self, data: List[NewVectorChunk], dimension: int) -> None:
        pass

    @abstractmethod
    async def get_by_collection_id_and_chunk_id(self, collection_id: str, chunk_id: Optional[str] = None) -> List[NewVectorChunk]:
        pass
