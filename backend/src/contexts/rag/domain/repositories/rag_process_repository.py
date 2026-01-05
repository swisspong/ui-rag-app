from typing import Any, Optional
from abc import ABC, abstractmethod

from src.contexts.rag.domain.entities.rag_process import RAGProcess
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID


class RAGProcessRepository(ABC):
    @abstractmethod
    async def save(self, data: RAGProcess, conn: Any = None) -> RAGProcess:
        pass

    @abstractmethod
    async def get_by_document_id_and_collection_id(self, document_id: DocumentID, collection_id: CollectionID, conn: Any = None) -> Optional[RAGProcess]:
        pass

    @abstractmethod
    async def get_by_collection_id_and_collection_file_id(self, collection_id: CollectionID, collection_file_id: CollectionFileID, conn: Any = None) -> Optional[RAGProcess]:
        pass
    