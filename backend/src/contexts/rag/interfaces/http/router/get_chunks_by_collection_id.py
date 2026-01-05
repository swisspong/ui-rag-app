from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_chunks_by_collection_id import (
    GetChunksByCollectionIdResponse,
    ChunksByCollectionIdData,
    ChunksByCollectionIdMeta,
    ChunkByCollectionIdItem
)
from src.contexts.rag.application.queries.get_chunks_by_collection_id.get_chunks_by_collection_id_query import GetChunksByCollectionIdQuery
from src.contexts.rag.application.queries.get_chunks_by_collection_id.get_chunks_by_collection_id_input import GetChunksByCollectionIdInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/collections/{collection_id}/chunks",
    response_model=GetChunksByCollectionIdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get chunks by collection id",
    description="Retrieves all chunks in a collection by collection_id"
)
@inject
async def get_chunks_by_collection_id(
    collection_id: str,
    get_chunks_by_collection_id_query: GetChunksByCollectionIdQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_chunks_by_collection_id_query]),
) -> GetChunksByCollectionIdResponse:
    input = GetChunksByCollectionIdInput(
        collection_id=CollectionID.from_value(collection_id)
    )
    result = await get_chunks_by_collection_id_query.execute(input)

    chunks_data = []
    for chunk in result.chunks:
        chunk_data = ChunkByCollectionIdItem(
            id=chunk.id,
            collection_id=chunk.collection_id,
            document_id=chunk.document_id,
            content=chunk.content,
            meta=chunk.meta,
            order_index=chunk.order_index,
            process_status=chunk.process_status,
            created_at=chunk.created_at,
            updated_at=chunk.updated_at
        )
        chunks_data.append(chunk_data)

    return GetChunksByCollectionIdResponse(
        data=ChunksByCollectionIdData(
            chunks=chunks_data
        ),
        meta=ChunksByCollectionIdMeta()
    )
