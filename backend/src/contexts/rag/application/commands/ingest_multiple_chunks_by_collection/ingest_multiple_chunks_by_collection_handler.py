import asyncio
from typing import List

import numpy as np

from src.contexts.rag.application.commands.ingest_multiple_chunks_by_collection.ingest_multiple_chunks_by_collection_input import (
    IngestMultipleChunksByCollectionInput,
)
from src.contexts.rag.application.commands.ingest_multiple_chunks_by_collection.ingest_multiple_chunks_by_collection_output import (
    IngestMultipleChunksByCollectionOutput,
    FailedChunk,
)
from src.contexts.rag.application.queries.get_collection.get_collection_input import (
    GetCollectionInput,
)
from src.contexts.rag.application.queries.get_collection.get_collection_query import (
    GetCollectionQuery,
)
from src.contexts.rag.domain.entities.new_chunk import Chunk
from src.contexts.rag.domain.entities.new_vector_chunk import NewVectorChunk
from src.contexts.rag.domain.errors.chunk_ingest_not_allowed import ChunkIngestNotAllowed
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.contexts.rag.domain.repositories.vector_repository import VectorRepository
from src.contexts.rag.domain.services.embedding import Embedding
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from src.contexts.rag.domain.value_objects.vector_chunk_id import VectorChunkID
from src.shared.application.errors import NotFound
from src.shared.ids.id_generator import IDGenerator


class IngestMultipleChunksByCollectionHandler:
    def __init__(
        self,
        chunk_repository: ChunkRepository,
        vector_repository: VectorRepository,
        embedding_service: Embedding,
        id_generator: IDGenerator,
        get_collection_query: GetCollectionQuery,
    ):
        self._chunk_repository = chunk_repository
        self._vector_repository = vector_repository
        self._embedding_service = embedding_service
        self._id_generator = id_generator
        self._get_collection_query = get_collection_query

    async def execute(
        self, input: IngestMultipleChunksByCollectionInput
    ) -> IngestMultipleChunksByCollectionOutput:
        # Validate input
        if not input.chunk_ids:
            return IngestMultipleChunksByCollectionOutput(
                success=True,
                ingested_chunk_ids=[],
                failed_chunks=[],
                total_count=0,
                ingested_count=0,
                failed_count=0,
            )

        # Verify collection exists
        collection_result = await self._get_collection_query.execute(
            GetCollectionInput(input.collection_id.value)
        )
        if not collection_result.collection:
            raise NotFound("Collection not found")

        # Fetch chunks by their IDs and collection ID
        chunks: List[Chunk] = []
        failed_chunks: List[FailedChunk] = []

        for chunk_id in input.chunk_ids:
            try:
                chunk = await self._chunk_repository.get_by_id_and_collection_id(
                    chunk_id=chunk_id, collection_id=input.collection_id
                )
                if chunk is None:
                    failed_chunks.append(
                        FailedChunk(
                            chunk_id=chunk_id.value,
                            error_message="Chunk not found",
                        )
                    )
                else:
                    # Validate that the chunk can be ingested
                    try:
                        chunk.ensure_can_ingest()
                        chunks.append(chunk)
                    except ChunkIngestNotAllowed as e:
                        failed_chunks.append(
                            FailedChunk(
                                chunk_id=chunk_id.value,
                                error_message=str(e),
                            )
                        )
            except Exception as e:
                failed_chunks.append(
                    FailedChunk(
                        chunk_id=chunk_id.value,
                        error_message=str(e),
                    )
                )

        # If no chunks to ingest, return early
        if not chunks:
            return IngestMultipleChunksByCollectionOutput(
                success=len(failed_chunks) == 0,
                ingested_chunk_ids=[],
                failed_chunks=failed_chunks,
                total_count=len(input.chunk_ids),
                ingested_count=0,
                failed_count=len(failed_chunks),
            )

        # Set chunks to RUNNING status
        for chunk in chunks:
            chunk.start_processing()
            await self._chunk_repository.save(chunk)

        # Prepare embedding parameters from collection config
        embedding_config = collection_result.collection.embedding_config
        max_batch_size = 10

        # Extract contents and create batches
        contents = [chunk.content for chunk in chunks]
        batches = [
            contents[i : i + max_batch_size]
            for i in range(0, len(contents), max_batch_size)
        ]

        # Generate embeddings in batches
        try:
            embedding_tasks = [
                self._embedding_service.embed(
                    batch,
                    model=embedding_config.model,
                    base_url=embedding_config.base_url,
                    api_key=embedding_config.api_key,
                )
                for batch in batches
            ]
            embeddings_list = await asyncio.gather(*embedding_tasks)
            embeddings = np.concatenate(embeddings_list)
            dimension = embeddings.shape[1]
        except Exception as e:
            # If embedding fails, mark all chunks as FAILED
            for chunk in chunks:
                chunk.fail_processing()
                await self._chunk_repository.save(chunk)
            failed_chunks.extend(
                [
                    FailedChunk(
                        chunk_id=chunk.id.value,
                        error_message=f"Embedding failed: {str(e)}",
                    )
                    for chunk in chunks
                ]
            )
            return IngestMultipleChunksByCollectionOutput(
                success=False,
                ingested_chunk_ids=[],
                failed_chunks=failed_chunks,
                total_count=len(input.chunk_ids),
                ingested_count=0,
                failed_count=len(failed_chunks),
            )

        # Create or update vector chunks (upsert logic)
        # Check if vector chunks exist before creating new ones
        vector_chunks = []
        for i, chunk in enumerate(chunks):
            try:
                # Check if a vector chunk already exists for this chunk_id and collection_id
                existing_vector_chunks = await self._vector_repository.get_by_collection_id_and_chunk_id(
                    collection_id=chunk.collection_id.value,
                    chunk_id=chunk.id.value
                )
                
                if existing_vector_chunks:
                    # Update existing vector chunk with new embedding, content, and meta
                    existing_vector_chunk = existing_vector_chunks[0]
                    existing_vector_chunk.vector = embeddings[i].tolist()
                    existing_vector_chunk.content = chunk.content
                    existing_vector_chunk.meta = chunk.meta
                    vector_chunks.append(existing_vector_chunk)
                else:
                    # Create new vector chunk using id_generator
                    vector_chunk_id = VectorChunkID.from_value(self._id_generator.new_id())
                    vector_chunk = NewVectorChunk.create(
                        id=vector_chunk_id,
                        chunk_id=chunk.id,
                        collection_id=chunk.collection_id,
                        vector=embeddings[i].tolist(),
                        content=chunk.content,
                        meta=chunk.meta,
                    )
                    vector_chunks.append(vector_chunk)
            except Exception as e:
                # Mark chunk as FAILED if vector chunk creation fails
                chunk.fail_processing()
                await self._chunk_repository.save(chunk)
                failed_chunks.append(
                    FailedChunk(
                        chunk_id=chunk.id.value,
                        error_message=f"Failed to create vector chunk: {str(e)}",
                    )
                )

        # Save vector chunks
        ingested_chunk_ids = []
        if vector_chunks:
            try:
                await self._vector_repository.saves(vector_chunks, dimension)
                ingested_chunk_ids = [vc.chunk_id.value for vc in vector_chunks]
                
                # Mark successfully ingested chunks as COMPLETED
                for vc in vector_chunks:
                    chunk = next((c for c in chunks if c.id == vc.chunk_id), None)
                    if chunk:
                        chunk.complete_processing()
                        await self._chunk_repository.save(chunk)
            except Exception as e:
                # If saving fails, mark all vector chunks as FAILED
                for vc in vector_chunks:
                    chunk = next((c for c in chunks if c.id == vc.chunk_id), None)
                    if chunk:
                        chunk.fail_processing()
                        await self._chunk_repository.save(chunk)
                    failed_chunks.append(
                        FailedChunk(
                            chunk_id=vc.chunk_id.value,
                            error_message=f"Failed to save vector chunk: {str(e)}",
                        )
                    )
                ingested_chunk_ids = []

        # Return output
        return IngestMultipleChunksByCollectionOutput(
            success=len(failed_chunks) == 0,
            ingested_chunk_ids=ingested_chunk_ids,
            failed_chunks=failed_chunks,
            total_count=len(input.chunk_ids),
            ingested_count=len(ingested_chunk_ids),
            failed_count=len(failed_chunks),
        )
