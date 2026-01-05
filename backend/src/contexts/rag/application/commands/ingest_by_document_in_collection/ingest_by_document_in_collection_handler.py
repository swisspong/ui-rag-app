
import asyncio

import numpy as np

from src.contexts.rag.application.commands.ingest_by_document_in_collection.ingest_by_document_in_collection_input import IngestionByDocumentInCollectionInput
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
from src.contexts.rag.domain.repositories.rag_process_repository import RAGProcessRepository
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


class IngestByDocumentInCollectionHandler:
    def __init__(
        self,
        embedding: Embedding,
        id_generator: IDGenerator,
        vector_repo: VectorRepository,
        get_collection_query: GetCollectionQuery,
        chunk_repository: ChunkRepository,
        rag_process_repository: RAGProcessRepository
    ):
        self._embedding = embedding
        self._id_generator = id_generator
        self._vector_repo = vector_repo
        self._get_collection_query = get_collection_query
        self._chunk_repo = chunk_repository
        self._rag_process_repo = rag_process_repository

    async def execute(self, input: IngestionByDocumentInCollectionInput) -> None:
        # document_id = DocumentID.from_value(input.document_id)
        collection_file_id = CollectionFileID.from_value(input.document_id)
        collection_id = CollectionID.from_value(input.collection_id)
        rag_process = await self._rag_process_repo.get_by_collection_id_and_collection_file_id(
            collection_id, collection_file_id)
        print(rag_process)
        # rag_process = await self._rag_process_repo.get_by_document_id_and_collection_id(
        #     document_id, collection_id)
        if not rag_process:
            raise NotFound("Rag process not found")
        document_id = rag_process.document_id
        collection_result = await self._get_collection_query.execute(GetCollectionInput(input.collection_id))
        if not collection_result.collection:
            raise NotFound("Collectin not found")

        chunks = await self._chunk_repo.get_by_document_id_in_collection(collection_id, document_id)
        
        # Mark all chunks as RUNNING before processing
        for chunk in chunks:
            chunk.start_processing()
            await self._chunk_repo.save(chunk)
        
        rag_process.start_ingest()
        await self._rag_process_repo.save(rag_process)
        max_batch_size = 10

        contents = [v.content for v in chunks]
        batches = [
            contents[i: i + max_batch_size]
            for i in range(0, len(contents), max_batch_size)
        ]

        embedding_tasks = [
            self._embedding.embed(
                batch,
                model=collection_result.collection.embedding_config.model,
                base_url=collection_result.collection.embedding_config.base_url,
                api_key=collection_result.collection.embedding_config.api_key,
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
                collection_id.value, d.id.value
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
        
        rag_process.finish_ingest()
        await self._rag_process_repo.save(rag_process)
