from typing import Any, List, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID

class ChunkReadRepository(ABC):
    @abstractmethod
    async def get_by_collection_and_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> List[ChunkReadModel]:
        pass

    @abstractmethod
    async def get_by_id_and_collection_id(self, chunk_id: str, collection_id: str, conn: Any = None) -> Optional[ChunkReadModel]:
        pass

    @abstractmethod
    async def get_by_collection_id(self, collection_id: CollectionID, conn: Any = None) -> List[ChunkReadModel]:
        pass
