from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_chunk_by_id_and_collection_id import (
    GetChunkByIdAndCollectionIdResponse,
    ChunkByIdAndCollectionIdData,
    ChunkByIdAndCollectionIdMeta
)
from src.contexts.rag.application.queries.get_chunk_by_id_and_collection_id.get_chunk_by_id_and_collection_id_query import GetChunkByIdAndCollectionIdQuery
from src.contexts.rag.application.queries.get_chunk_by_id_and_collection_id.get_chunk_by_id_and_collection_id_input import GetChunkByIdAndCollectionIdInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/collections/{collection_id}/chunks/{chunk_id}",
    response_model=GetChunkByIdAndCollectionIdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get chunk by id and collection id",
    description="Retrieves a single chunk in a collection by chunk_id and collection_id"
)
@inject
async def get_chunk_by_id_and_collection_id(
    collection_id: str,
    chunk_id: str,
    get_chunk_by_id_and_collection_id_query: GetChunkByIdAndCollectionIdQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_chunk_by_id_and_collection_id_query]),
) -> GetChunkByIdAndCollectionIdResponse:
    input = GetChunkByIdAndCollectionIdInput(
        chunk_id=ChunkID.from_value(chunk_id),
        collection_id=CollectionID.from_value(collection_id)
    )
    result = await get_chunk_by_id_and_collection_id_query.execute(input)

    chunk_data = None
    if result is not None:
        chunk_data = {
            "id": result.id,
            "collection_id": result.collection_id,
            "document_id": result.document_id,
            "content": result.content,
            "meta": result.meta,
            "order_index": result.order_index,
            "process_status": result.process_status,
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    return GetChunkByIdAndCollectionIdResponse(
        data=ChunkByIdAndCollectionIdData(
            chunk=chunk_data
        ),
        meta=ChunkByIdAndCollectionIdMeta()
    )
