from typing import Any, List, Optional
from src.contexts.rag.application.queries.repoistories.chunk_read_repository import ChunkReadRepository
from src.contexts.rag.application.queries.models.additional_chunk_read_model import AdditionalChunkReadModel
from src.contexts.rag.application.queries.get_additional_chunks.get_additional_chunks_input import GetAdditionalChunksInput


class GetAdditionalChunksQuery:
    def __init__(self, chunk_read_repository: ChunkReadRepository):
        self._chunk_read_repository = chunk_read_repository

    async def execute(self, input_data: GetAdditionalChunksInput, conn: Any = None) -> dict:
        offset = (input_data.page - 1) * input_data.limit
        
        chunks, total = await self._chunk_read_repository.get_additional_chunks(
            collection_id=input_data.collection_id,
            offset=offset,
            limit=input_data.limit,
            search=input_data.search,
            conn=conn
        )

        total_pages = (total + input_data.limit - 1) // input_data.limit
        has_next_page = input_data.page < total_pages
        has_previous_page = input_data.page > 1

        return {
            "data": chunks,
            "metadata": {
                "page": input_data.page,
                "limit": input_data.limit,
                "total": total,
                "totalPages": total_pages,
                "hasNextPage": has_next_page,
                "hasPreviousPage": has_previous_page,
            }
        }
