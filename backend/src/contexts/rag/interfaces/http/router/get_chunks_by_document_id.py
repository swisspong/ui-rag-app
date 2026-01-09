from math import ceil
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_chunks_by_document_id import (
    GetChunksByDocumentIdResponse,
    ChunkItem,
    PaginationMeta
)
from src.contexts.rag.application.queries.get_document_chunks.get_document_chunks_input import (
    GetDocumentChunksInput
)
from src.contexts.rag.application.queries.get_document_chunks.get_document_chunks_query import (
    GetDocumentChunksQuery
)
from src.boot.container import ApplicationContainer

from . import router


@router.get(
    "/collections/{collection_id}/documents/{document_id}/version/{version}/chunks",
    response_model=GetChunksByDocumentIdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document chunks",
    description="Retrieves a list of chunks for a specific document version with pagination"
)
@inject
async def get_chunks_by_document_id(
    collection_id: str,
    document_id: str,
    version: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = Query(None),
    get_document_chunks_query: GetDocumentChunksQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_document_chunks_query]
    ),
) -> GetChunksByDocumentIdResponse:
    offset = (page - 1) * limit

    query = GetDocumentChunksInput(
        collection_id=collection_id,
        document_id=document_id,
        version=version,
        offset=offset,
        limit=limit,
        search=search,
    )

    result = await get_document_chunks_query.execute(query)

    total_pages = ceil(result.total / limit) if limit > 0 else 0

    return GetChunksByDocumentIdResponse(
        data=[
            ChunkItem(
                id=item.id,
                content=item.content,
                meta=item.meta,
                status=item.status
            )
            for item in result.data
        ],
        metadata=PaginationMeta(
            page=page,
            limit=limit,
            total=result.total,
            totalPages=total_pages,
            hasNextPage=page < total_pages,
            hasPreviousPage=page > 1
        )
    )
