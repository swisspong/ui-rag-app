from typing import Any, List, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.document_read_model import DocumentReadModel
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID


class DocumentReadRepository(ABC):
    @abstractmethod
    @abstractmethod
    async def get_by_collection_id(
        self,
        collection_id: CollectionID,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
        select: bool = False,
        conn: Any = None
    ) -> List[DocumentReadModel]:
        pass

    @abstractmethod
    async def count_by_collection_id(
        self,
        collection_id: CollectionID,
        search: Optional[str] = None,
        conn: Any = None
    ) -> int:
        pass
