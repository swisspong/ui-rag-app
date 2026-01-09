from typing import List, Tuple

from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository
from src.contexts.rag.application.queries.get_document_chunks_in_collection.get_document_chunks_in_collection_input import GetDocumentChunksInCollectionInput
from src.contexts.rag.application.queries.get_document_chunks_in_collection.get_document_chunks_in_collection_output import GetDocumentChunksInCollectionOutput


class GetDocumentChunksInCollectionQuery:
    def __init__(
        self,
        chunk_read_repository: ChunkReadRepository
    ):
        self._chunk_read_repository = chunk_read_repository

    async def execute(self, input: GetDocumentChunksInCollectionInput) -> GetDocumentChunksInCollectionOutput:
        data, total = await self._chunk_read_repository.get_document_summaries_by_collection_id(
            collection_id=input.collection_id,
            offset=input.offset,
            limit=input.limit,
            search=input.search
        )

        return GetDocumentChunksInCollectionOutput(
            data=data,
            total=total,
            offset=input.offset,
            limit=input.limit
        )
