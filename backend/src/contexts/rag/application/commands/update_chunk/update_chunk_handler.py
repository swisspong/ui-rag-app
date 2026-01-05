from typing import Optional

from src.contexts.rag.application.commands.update_chunk.update_chunk_input import UpdateChunkInput
from src.contexts.rag.application.commands.update_chunk.update_chunk_output import UpdateChunkOutput
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.contexts.rag.domain.entities.new_chunk import Chunk
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.shared.application.errors import NotFound


class UpdateChunkHandler:
    def __init__(
        self,
        chunk_repository: ChunkRepository
    ):
        self._chunk_repository = chunk_repository

    async def execute(self, input: UpdateChunkInput) -> Optional[UpdateChunkOutput]:
        # Retrieve the chunk using the write repository
        chunk = await self._chunk_repository.get_by_id_and_collection_id(
            chunk_id=input.chunk_id,
            collection_id=input.collection_id
        )

        if chunk is None:
            raise NotFound("Chunk not found")

        # Update the chunk using the domain entity's update method
        # Set process_status to pending to indicate the chunk needs to be re-processed/ingested
        chunk.update(content=input.content, meta=input.meta, process_status=ProcessStatus.PENDING)

        # Save the updated chunk
        saved_chunk = await self._chunk_repository.save(chunk)

        # Return the output
        return UpdateChunkOutput(
            id=saved_chunk.id.value,
            collection_id=saved_chunk.collection_id.value,
            document_id=saved_chunk.document_id.value,
            content=saved_chunk.content,
            meta=saved_chunk.meta,
            order_index=saved_chunk.order_index,
            created_at=saved_chunk.created_at,
            updated_at=saved_chunk.updated_at
        )
