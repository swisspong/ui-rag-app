from typing import Any, List, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.domain.entities.new_chunk import Chunk
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus


class ChunkRepository(ABC):
    @abstractmethod
    async def save(self, data: Chunk, conn: Any = None) -> Chunk:
        pass


    @abstractmethod
    async def get_by_document_id_in_collection(self, collection_id: CollectionID, document_id: DocumentID, version: int, status: ProcessStatus, conn: Any = None) -> List[Chunk]:
        pass

    @abstractmethod
    async def get_by_id_and_collection_id(self, chunk_id: ChunkID, collection_id: CollectionID, conn: Any = None) -> Optional[Chunk]:
        pass

    @abstractmethod
    async def delete_by_id_and_collection_id(self, chunk_id: ChunkID, collection_id: CollectionID, conn: Any = None) -> bool:
        pass

    @abstractmethod
    async def delete_multiple_by_ids_and_collection_id(self, chunk_ids: List[ChunkID], collection_id: CollectionID, conn: Any = None) -> int:
        pass

    @abstractmethod
    async def get_latest_version_by_document_id(self, collection_id: CollectionID, document_id: DocumentID, conn: Any = None) -> Optional[int]:
        pass
