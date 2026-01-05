from abc import ABC, abstractmethod
from typing import List
from src.contexts.rag.domain.entities.chunk import DocChunk


class KVRepository(ABC):
    @abstractmethod
    async def upsert_text_chunk(self, data: List[DocChunk], conn=None) -> None:
        pass
