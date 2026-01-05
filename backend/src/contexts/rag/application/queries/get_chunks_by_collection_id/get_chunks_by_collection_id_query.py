from typing import List

from src.contexts.rag.application.queries.get_chunks_by_collection_id.get_chunks_by_collection_id_input import GetChunksByCollectionIdInput
from src.contexts.rag.application.queries.get_chunks_by_collection_id.get_chunks_by_collection_id_output import GetChunksByCollectionIdOutput
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository


class GetChunksByCollectionIdQuery:
    def __init__(
        self,
        chunk_read_repository: ChunkReadRepository
    ):
        self._chunk_read_repository = chunk_read_repository

    async def execute(self, input: GetChunksByCollectionIdInput) -> GetChunksByCollectionIdOutput:
        chunks = await self._chunk_read_repository.get_by_collection_id(
            collection_id=input.collection_id
        )
        return GetChunksByCollectionIdOutput(chunks=chunks)
