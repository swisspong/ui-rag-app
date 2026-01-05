from typing import List

from src.contexts.rag.application.queries.get_chunks_by_collection_file_id.get_chunks_by_collection_file_id_input import GetChunksByCollectionFileIdInput
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository


class GetChunksByCollectionFileIdQuery:
    def __init__(
        self,
        chunk_read_repository: ChunkReadRepository
    ):
        self._chunk_read_repository = chunk_read_repository

    async def execute(self, input: GetChunksByCollectionFileIdInput) -> List[ChunkReadModel]:
        return await self._chunk_read_repository.get_by_collection_and_file_id(
            collection_id=input.collection_id,
            collection_file_id=input.collection_file_id
        )
