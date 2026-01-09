from fastapi import APIRouter, Depends, Query, Request
from dependency_injector.wiring import inject, Provide
from typing import Optional

from src.boot.container import ApplicationContainer
from src.contexts.rag.application.queries.get_document_chunks_in_collection.get_document_chunks_in_collection_query import GetDocumentChunksInCollectionQuery
from src.contexts.rag.application.queries.get_document_chunks_in_collection.get_document_chunks_in_collection_input import GetDocumentChunksInCollectionInput
from src.contexts.rag.application.queries.get_document_chunks_in_collection.get_document_chunks_in_collection_output import GetDocumentChunksInCollectionOutput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.interfaces.http.schema.get_document_chunks_in_collection import (
    GetDocumentChunksInCollectionResponse,
    DocumentChunkItem,
    DocumentChunkListMetadata
)

from . import router


@router.get("/{collection_id}/documentChunks", response_model=GetDocumentChunksInCollectionResponse)
@inject
async def get_document_chunks_in_collection(
    request: Request,
    collection_id: str,
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(10, description="Number of items per page"),
    search: Optional[str] = Query(
        None, description="Search term for filtering"),
    query: GetDocumentChunksInCollectionQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_document_chunks_in_collection_query])
) -> GetDocumentChunksInCollectionResponse:
    input_dto = GetDocumentChunksInCollectionInput(
        collection_id=CollectionID(collection_id),
        offset=offset,
        limit=limit,
        search=search
    )
    result: GetDocumentChunksInCollectionOutput = await query.execute(input_dto)

    return GetDocumentChunksInCollectionResponse(
        data=[
            DocumentChunkItem(
                id=item.id,
                version=item.version,
                name=item.name,
                chunk_count=item.chunk_count,
                created_at=item.created_at
            )
            for item in result.data
        ],
        metadata=DocumentChunkListMetadata(
            offset=result.offset,
            limit=result.limit,
            total=result.total,
            has_next_page=(result.offset + result.limit) < result.total,
            has_previous_page=result.offset > 0
        )
    )
