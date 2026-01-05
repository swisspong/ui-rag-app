from typing import Any
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.collection_read_model import CollectionReadModel


class CollectionReadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, conn: Any = None) -> CollectionReadModel:
        pass
