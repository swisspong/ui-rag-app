import time
import asyncio

import numpy as np

from src.contexts.rag.application.commands.embed.embed_input import EmbedInput
from src.shared.ids.id_generator import IDGenerator
from src.contexts.rag.domain.services.tokenizer import Tokenizer
from src.contexts.rag.domain.entities.chunk import DocChunk
from src.contexts.rag.domain.entities.vector_chunk import VectorChunk
from src.contexts.rag.domain.repositories.kv_repoisory import KVRepository
from src.contexts.rag.domain.repositories.vector_repository import VectorRepository
from src.contexts.rag.domain.services.embedding import Embedding


class Embed:
    def __init__(
        self,
        embedding: Embedding,
        tokenizer: Tokenizer,
        id_generator: IDGenerator,
        kv_repo: KVRepository,
        vector_repo: VectorRepository
    ):
        self._embedding = embedding
        self._tokenizer = tokenizer
        self._id_generator = id_generator
        self._kv_repo = kv_repo
        self._vector_repo = vector_repo

    async def execute(self, input: EmbedInput) -> None:
        
        max_token_size = input.max_token_size
        overlap_token_size = input.overlap_token_size
        max_batch_size = input.max_batch_size
        doc_id = input.doc_id
        file_path = input.file_path
        workspace = input.workspace
        
        #  kv store
        # 1. sinitize text
        text = input.content
        # 2. encode
        tokens = self._tokenizer.encode(text)

        results = []
        for index, start in enumerate(
            range(0, len(tokens), max_token_size - overlap_token_size)
        ):
            chunk_content = self._tokenizer.decode(
                tokens[start: start + max_token_size])
            results.append(
                {
                    "tokens": min(max_token_size, len(tokens) - start),
                    "content": chunk_content.strip(),
                    "chunk_order_index": index,
                }
            )

        chunks = [
            DocChunk.create(
                tokens=dp["tokens"],
                content=dp["content"],
                chunk_order_index=dp["chunk_order_index"],
                full_doc_id=doc_id,
                file_path=file_path,
                workspace=workspace
            ) for dp in results
        ]

        await self._kv_repo.upsert_text_chunk(chunks)


        # vector store

        contents = [v.content for v in chunks]
        batches = [
            contents[i: i + max_batch_size]
            for i in range(0, len(contents), max_batch_size)
        ]

        embedding_tasks = [self._embedding.embed(batch) for batch in batches]
        embeddings_list = await asyncio.gather(*embedding_tasks)

        embeddings = np.concatenate(embeddings_list)

        current_time = int(time.time())

        list_data = [
            {
                "id": chunk.id,
                "create_at": current_time,
                "content": chunk.content,
                "file_path": chunk.file_path,
                "full_doc_id": chunk.full_doc_id
            }
            for chunk in chunks
        ]
        vector_chunks = []
        for i, d in enumerate(list_data):

            d["vector"] = embeddings[i]
            vector_chunks.append(
                VectorChunk.create(
                id=d['id'],
                vector=d['vector'],
                content=d['content'],
                file_path=d['file_path'],
                full_doc_id=d['full_doc_id']
                )
            )

        await self._vector_repo.upsert(workspace,vector_chunks)