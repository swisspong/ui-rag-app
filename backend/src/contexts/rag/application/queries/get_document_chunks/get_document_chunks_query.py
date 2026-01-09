from src.contexts.rag.application.queries.get_document_chunks.get_document_chunks_input import GetDocumentChunksInput
from src.contexts.rag.application.queries.get_document_chunks.get_document_chunks_output import GetDocumentChunksOutput
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository


class GetDocumentChunksQuery:
    def __init__(self, chunk_read_repository: ChunkReadRepository):
        self.chunk_read_repository = chunk_read_repository

    async def execute(self, input: GetDocumentChunksInput) -> GetDocumentChunksOutput:

        chunks, total = await self.chunk_read_repository.get_chunks_by_collection_file_id(
            collection_id=input.collection_id,
            document_id=input.document_id,
            version=input.version,
            offset=input.offset,
            limit=input.limit,
            search=input.search
        )
        return GetDocumentChunksOutput(
            data=chunks,
            total=total
        )
