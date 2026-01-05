from typing import Optional

from src.contexts.rag.application.queries.get_chunk_by_id_and_collection_id.get_chunk_by_id_and_collection_id_input import GetChunkByIdAndCollectionIdInput
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository


class GetChunkByIdAndCollectionIdQuery:
    def __init__(
        self,
        chunk_read_repository: ChunkReadRepository
    ):
        self._chunk_read_repository = chunk_read_repository

    async def execute(self, input: GetChunkByIdAndCollectionIdInput) -> Optional[ChunkReadModel]:
        chunk = await self._chunk_read_repository.get_by_id_and_collection_id(
            chunk_id=input.chunk_id.value,
            collection_id=input.collection_id.value
        )
        return chunk
