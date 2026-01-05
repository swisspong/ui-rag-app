from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_chunks_by_collection_file_id import (
    GetChunksByCollectionFileIdResponse,
    ChunkItem,
    ChunksByCollectionFileIdData,
    ChunksByCollectionFileIdMeta
)
from src.contexts.rag.application.queries.get_chunks_by_collection_file_id.get_chunks_by_collection_file_id_query import GetChunksByCollectionFileIdQuery
from src.contexts.rag.application.queries.get_chunks_by_collection_file_id.get_chunks_by_collection_file_id_input import GetChunksByCollectionFileIdInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/collections/{collection_id}/collection-files/{collection_file_id}/chunks",
    response_model=GetChunksByCollectionFileIdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get chunks by collection file id",
    description="Retrieves a list of chunks for a specific collection file in a collection"
)
@inject
async def get_chunks_by_collection_file_id(
    collection_id: str,
    collection_file_id: str,
    get_chunks_by_collection_file_id_query: GetChunksByCollectionFileIdQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_chunks_by_collection_file_id_query]),
) -> GetChunksByCollectionFileIdResponse:
    input = GetChunksByCollectionFileIdInput(
        collection_id=CollectionID.from_value(collection_id),
        collection_file_id=CollectionFileID.from_value(collection_file_id)
    )
    result = await get_chunks_by_collection_file_id_query.execute(input)

    return GetChunksByCollectionFileIdResponse(
        data=ChunksByCollectionFileIdData(
            chunks=[
                {
                    "id": chunk.id,
                    "collection_id": chunk.collection_id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "meta": chunk.meta,
                    "process_status": chunk.process_status
                }
                for chunk in result
            ]
        ),
        meta=ChunksByCollectionFileIdMeta()
    )
