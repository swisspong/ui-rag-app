from typing import Any, List, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.document_read_model import DocumentReadModel
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID


class DocumentReadRepository(ABC):
    @abstractmethod
    async def get_by_collection_id(self, collection_id: CollectionID, conn: Any = None) -> List[DocumentReadModel]:
        pass

    @abstractmethod
    async def get_by_collection_and_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> Optional[DocumentReadModel]:
        pass
