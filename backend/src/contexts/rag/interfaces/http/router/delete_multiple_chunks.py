from fastapi import Depends, status, Query
from typing import List
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.delete_multiple_chunks import (
    DeleteMultipleChunksResponse,
    DeleteMultipleChunksData,
    DeleteMultipleChunksMeta
)
from src.contexts.rag.application.commands.delete_multiple_chunks.delete_multiple_chunks_handler import DeleteMultipleChunksHandler
from src.contexts.rag.application.commands.delete_multiple_chunks.delete_multiple_chunks_input import DeleteMultipleChunksInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.boot.container import ApplicationContainer
from . import router


@router.delete(
    "/collections/{collection_id}/chunks",
    response_model=DeleteMultipleChunksResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete multiple chunks by collection ID and chunk IDs",
    description="Deletes multiple chunks in a collection by collection_id and a list of chunk_ids"
)
@inject
async def delete_multiple_chunks(
    collection_id: str,
    chunk_ids: List[str] = Query(..., description="List of chunk IDs to delete"),
    delete_multiple_chunks_handler: DeleteMultipleChunksHandler = Depends(
        Provide[ApplicationContainer.rag_package.delete_multiple_chunks_handler]),
) -> DeleteMultipleChunksResponse:
    input = DeleteMultipleChunksInput(
        collection_id=CollectionID.from_value(collection_id),
        chunk_ids=[ChunkID.from_value(chunk_id) for chunk_id in chunk_ids]
    )
    result = await delete_multiple_chunks_handler.execute(input)

    return DeleteMultipleChunksResponse(
        data=DeleteMultipleChunksData(
            deleted_chunk_ids=result.deleted_chunk_ids,
            deleted_count=result.deleted_count
        ),
        meta=DeleteMultipleChunksMeta()
    )
