from typing import Any, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.domain.entities.document import Document
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


class DocumentRepository(ABC):
    @abstractmethod
    async def save(self, data: Document, conn: Any = None) -> Document:
        pass

    @abstractmethod
    async def get_by_id(self, document_id: DocumentID, conn: Any = None) -> Optional[Document]:
        pass

    @abstractmethod
    async def get_many_by_collection_id(self, collection_id: CollectionID, conn: Any = None) -> list[Document]:
        pass
