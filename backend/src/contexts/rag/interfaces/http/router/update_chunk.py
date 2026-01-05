from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.update_chunk import (
    UpdateChunkResponse,
    UpdateChunkData,
    UpdateChunkMeta,
    UpdateChunkRequest
)
from src.contexts.rag.application.commands.update_chunk.update_chunk_handler import UpdateChunkHandler
from src.contexts.rag.application.commands.update_chunk.update_chunk_input import UpdateChunkInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.boot.container import ApplicationContainer
from . import router


@router.put(
    "/collections/{collection_id}/chunks/{chunk_id}",
    response_model=UpdateChunkResponse,
    status_code=status.HTTP_200_OK,
    summary="Update chunk by id and collection id",
    description="Updates a single chunk in a collection by chunk_id and collection_id"
)
@inject
async def update_chunk(
    collection_id: str,
    chunk_id: str,
    request: UpdateChunkRequest,
    update_chunk_handler: UpdateChunkHandler = Depends(
        Provide[ApplicationContainer.rag_package.update_chunk_handler]),
) -> UpdateChunkResponse:
    input = UpdateChunkInput(
        chunk_id=ChunkID.from_value(chunk_id),
        collection_id=CollectionID.from_value(collection_id),
        content=request.content,
        meta=request.meta
    )
    result = await update_chunk_handler.execute(input)

    chunk_data = {
        "id": result.id,
        "collection_id": result.collection_id,
        "document_id": result.document_id,
        "content": result.content,
        "meta": result.meta,
        "order_index": result.order_index,
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }

    return UpdateChunkResponse(
        data=UpdateChunkData(
            chunk=chunk_data
        ),
        meta=UpdateChunkMeta()
    )
