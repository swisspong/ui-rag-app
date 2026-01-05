from src.contexts.rag.application.commands.delete_multiple_chunks.delete_multiple_chunks_input import DeleteMultipleChunksInput
from src.contexts.rag.application.commands.delete_multiple_chunks.delete_multiple_chunks_output import DeleteMultipleChunksOutput
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.shared.application.errors import NotFound


class DeleteMultipleChunksHandler:
    def __init__(
        self,
        chunk_repository: ChunkRepository
    ):
        self._chunk_repository = chunk_repository

    async def execute(self, input: DeleteMultipleChunksInput) -> DeleteMultipleChunksOutput:
        if not input.chunk_ids:
            return DeleteMultipleChunksOutput(
                deleted_chunk_ids=[],
                deleted_count=0
            )

        # Delete multiple chunks by their IDs and collection ID
        deleted_count = await self._chunk_repository.delete_multiple_by_ids_and_collection_id(
            chunk_ids=input.chunk_ids,
            collection_id=input.collection_id
        )

        # Return the output with deleted chunk IDs and count
        return DeleteMultipleChunksOutput(
            deleted_chunk_ids=[chunk_id.value for chunk_id in input.chunk_ids],
            deleted_count=deleted_count
        )
