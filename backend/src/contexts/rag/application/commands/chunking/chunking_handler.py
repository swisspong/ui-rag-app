from src.contexts.rag.domain.services.tokenizer import Tokenizer
from src.contexts.rag.domain.repositories.chunk_repository import ChunkRepository
from src.contexts.rag.domain.repositories.document_repository import DocumentRepository
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.application.commands.chunking.chunking_input import ChunkingInput
from src.contexts.rag.domain.entities.new_chunk import Chunk
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.shared.domain.services.id_generator import IDGenerator
from src.shared.application.errors import NotFound


class ChunkingHandler:
    def __init__(
        self,
        tokenizer: Tokenizer,
        chunk_repository: ChunkRepository,
        document_repository: DocumentRepository,
        id_generator: IDGenerator
    ):
        self._tokenizer = tokenizer
        self._chunk_repo = chunk_repository
        self._document_repo = document_repository
        self._id_generator = id_generator

    async def execute(self, input: ChunkingInput):
        collection_id = CollectionID.from_value(input.collection_id)
        print("in chunking handler")
        for doc_id_str in input.document_ids:
            print(doc_id_str)
            print(doc_id_str)
            document_id = DocumentID.from_value(doc_id_str)

            document = await self._document_repo.get_by_id(document_id)
            if not document:
                raise NotFound("Document not found")
            document = await self._document_repo.get_by_id(document_id)
            print("test test")
            print(document)
            if not document_id:
                raise ValueError()

            # Delete existing chunks for this document before creating new ones
            # existing_chunks = await self._chunk_repo.get_by_document_id_in_collection(
            #     collection_id, document_id
            # )
            # if existing_chunks:
            #     chunk_ids = [chunk.id for chunk in existing_chunks]
            #     await self._chunk_repo.delete_multiple_by_ids_and_collection_id(
            #         chunk_ids, collection_id
            #     )

            latest_version = await self._chunk_repo.get_latest_version_by_document_id(collection_id, document_id)
            new_version = (latest_version or 0) + 1

            tokens = self._tokenizer.encode(document.content)
            # chunks: List[Chunk] = []
            for index, start in enumerate(
                range(0, len(tokens), input.max_token_size -
                      input.overlap_token_size)
            ):
                chunk_content = self._tokenizer.decode(
                    tokens[start: start + input.max_token_size])
                # chunks.append(

                # )
                chunk = Chunk.create(
                    id=ChunkID.from_value(self._id_generator.new_id()),
                    collection_id=collection_id,
                    document_id=document_id,
                    order_index=index,
                    content=chunk_content,
                    meta={
                        # "order_index": index
                    },
                    version=new_version
                )
                await self._chunk_repo.save(chunk)
            # results.append(
            #     {
            #         "tokens": min(input.max_token_size, len(tokens) - start),
            #         "content": chunk_content.strip(),
            #         "chunk_order_index": index,
            #     }
            # )
