from typing import Any, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.collection_file_read_model import CollectionFileReadModel


class CollectionFileReadRepository(ABC):
    @abstractmethod
    async def get_by_collection_and_file_id(self, collection_id: str, collection_file_id: str, conn: Any = None) -> Optional[CollectionFileReadModel]:
        pass
