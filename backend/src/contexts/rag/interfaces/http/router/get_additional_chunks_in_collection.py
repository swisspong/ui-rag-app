from fastapi import APIRouter, Depends, Query, Request
from dependency_injector.wiring import inject, Provide
from typing import Optional


from src.boot.container import ApplicationContainer
from src.contexts.rag.application.queries.get_additional_chunks.get_additional_chunks_query import GetAdditionalChunksQuery
from src.contexts.rag.application.queries.get_additional_chunks.get_additional_chunks_input import GetAdditionalChunksInput
from src.contexts.rag.interfaces.http.schema.get_additional_chunks_in_collection import (
    GetAdditionalChunksInCollectionResponse,
    AdditionalChunkItem,
    AdditionalChunkListMetadata
)

from . import router


@router.get("/{collection_id}/additional-chunks", response_model=GetAdditionalChunksInCollectionResponse)
@inject
async def get_additional_chunks_in_collection(
    request: Request,
    collection_id: str,
    page: int = Query(1, description="Page number for pagination", ge=1),
    limit: int = Query(10, description="Number of items per page", le=100),
    search: Optional[str] = Query(
        None, description="Search term for filtering"),
    query: GetAdditionalChunksQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_additional_chunks_query])
) -> GetAdditionalChunksInCollectionResponse:
    input_dto = GetAdditionalChunksInput(
        collection_id=collection_id,
        page=page,
        limit=limit,
        search=search
    )
    result = await query.execute(input_dto)

    metadata = result['metadata']
    
    return GetAdditionalChunksInCollectionResponse(
        data=[
            AdditionalChunkItem(
                id=item.id,
                content=item.content,
                meta=item.meta,
                status=item.status,
                version=item.version,
                createdAt=item.created_at
            )
            for item in result['data']
        ],
        metadata=AdditionalChunkListMetadata(
            page=metadata['page'],
            limit=metadata['limit'],
            total=metadata['total'],
            totalPages=metadata['totalPages'],
            hasNextPage=metadata['hasNextPage'],
            hasPreviousPage=metadata['hasPreviousPage']
        )
    )
