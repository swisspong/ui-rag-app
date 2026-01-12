from typing import Any, List, Optional
from abc import ABC, abstractmethod
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.application.queries.models.document_chunk_summary_read_model import DocumentChunkSummaryReadModel
from src.contexts.rag.application.queries.models.document_chunk_read_model import DocumentChunkReadModel
from src.contexts.rag.application.queries.models.additional_chunk_read_model import AdditionalChunkReadModel
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

    @abstractmethod
    async def get_document_summaries_by_collection_id(
        self,
        collection_id: CollectionID,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        conn: Any = None
    ) -> tuple[List[DocumentChunkSummaryReadModel], int]:
        pass

    @abstractmethod
    async def get_chunks_by_collection_file_id(
        self,
        collection_id: str,
        document_id: str,
        version: int,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        conn: Any = None
    ) -> tuple[List[DocumentChunkReadModel], int]:
        pass

    @abstractmethod
    async def get_additional_chunks(
        self,
        collection_id: str,
        offset: int,
        limit: int,
        search: Optional[str] = None,
        conn: Any = None
    ) -> tuple[List['AdditionalChunkReadModel'], int]:
        pass
