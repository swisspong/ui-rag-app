
import asyncio

import numpy as np
from typing import Any, Optional

from src.contexts.rag.application.commands.embed_by_document_in_collection.embed_by_document_in_collection_input import EmbedByDocumentInCollectionInput
from src.shared.ids.id_generator import IDGenerator
from src.contexts.rag.domain.entities.new_vector_chunk import NewVectorChunk
from src.contexts.rag.domain.value_objects.vector_chunk_id import VectorChunkID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.repositories.vector_repository import VectorRepository
from src.contexts.rag.domain.services.embedding import Embedding
from src.contexts.rag.application.queries.get_collection.get_collection_input import GetCollectionInput
from src.contexts.rag.application.queries.get_collection.get_collection_query import GetCollectionQuery
from src.shared.application.errors import NotFound
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.errors.chunk_ingest_not_allowed import ChunkIngestNotAllowed
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus


class EmbedByDocumentInCollectionHandler:
    def __init__(
        self,
        enable_config_mode: bool,
        embedding_model: str,
        embedding_base_url: Optional[str],
        embedding_api_key: str,
        embedding: Embedding,
        id_generator: IDGenerator,
        vector_repo: VectorRepository,
        get_collection_query: GetCollectionQuery,
        chunk_repository: ChunkRepository
    ):
        self._enable_config_mode = enable_config_mode
        self._embedding_api_key = embedding_api_key
        self._embedding_base_url = embedding_base_url
        self._embedding_model = embedding_model
        self._embedding = embedding
        self._id_generator = id_generator
        self._vector_repo = vector_repo
        self._get_collection_query = get_collection_query
        self._chunk_repo = chunk_repository

    async def execute(self, input: EmbedByDocumentInCollectionInput) -> None:
        if input.status in (ProcessStatus.RUNNING, ProcessStatus.COMPLETED):
             raise ChunkIngestNotAllowed(process_status=input.status.value)

        collection_result = await self._get_collection_query.execute(GetCollectionInput(input.collection_id.value))
        if not collection_result.collection:
            raise NotFound("Collectin not found")

        chunks = await self._chunk_repo.get_by_document_id_in_collection(
            input.collection_id,
            input.document_id,
            input.version,
            input.status
        )
        print(chunks)
        if len(chunks) <= 0:
            raise NotFound("Chunks not found")
        # Mark all chunks as RUNNING before processing
        for chunk in chunks:
            chunk.start_processing()
            await self._chunk_repo.save(chunk)
        max_batch_size = 10

        contents = [v.content for v in chunks]
        batches = [
            contents[i: i + max_batch_size]
            for i in range(0, len(contents), max_batch_size)
        ]
        if self._enable_config_mode is False:
            embedding_model = self._embedding_model
            embedding_api_key = self._embedding_api_key
            embedding_base_url = self._embedding_base_url
        else:
            embedding_model = collection_result.collection.embedding_config.model
            embedding_api_key = collection_result.collection.embedding_config.api_key
            embedding_base_url = collection_result.collection.embedding_config.base_url

        embedding_tasks = [
            self._embedding.embed(
                batch,
                model=embedding_model,
                base_url=embedding_base_url,
                api_key=embedding_api_key,
            )
            for batch in batches
        ]
        embeddings_list = await asyncio.gather(*embedding_tasks)

        embeddings = np.concatenate(embeddings_list)
        dimension = embeddings.shape[1]
        vector_chunks = []
        for i, d in enumerate(chunks):
            # Check if a vector chunk already exists for this chunk_id
            existing_vector_chunks = await self._vector_repo.get_by_collection_id_and_chunk_id(
                input.collection_id.value, d.id.value
            )
            
            if existing_vector_chunks:
                # Update existing vector chunk with new embedding, content, and metadata
                existing_vector_chunk = existing_vector_chunks[0]
                vector_chunks.append(
                    NewVectorChunk(
                        id=existing_vector_chunk.id,
                        chunk_id=d.id,
                        collection_id=d.collection_id,
                        vector=embeddings[i],
                        content=d.content,
                        meta=d.meta,
                        created_at=existing_vector_chunk.created_at
                    )
                )
            else:
                # Create new vector chunk with new ID
                vector_chunks.append(
                    NewVectorChunk.create(
                        id=VectorChunkID.from_value(self._id_generator.new_id()),
                        chunk_id=d.id,
                        collection_id=d.collection_id,
                        vector=embeddings[i],
                        content=d.content,
                        meta=d.meta
                    )
                )

        await self._vector_repo.saves(vector_chunks, dimension)
        
        # Mark all chunks as COMPLETED after successful vector creation
        for chunk in chunks:
            chunk.complete_processing()
            await self._chunk_repo.save(chunk)