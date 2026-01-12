from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_documents_in_collection import (
    GetDocumentsInCollectionResponse,
    DocumentsInCollectionMeta
)
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_query import GetDocumentsInCollectionQuery
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_input import GetDocumentsInCollectionInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/{collection_id}/documents",
    response_model=GetDocumentsInCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get documents in collection",
    description="Retrieves a list of documents in a collection"
)
@inject
async def get_documents_in_collection(
    collection_id: str,
    page: int = 1,
    limit: int = 10,
    search: str = None,
    select: bool = False,
    get_documents_in_collection_query: GetDocumentsInCollectionQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_documents_in_collection_query]),
) -> GetDocumentsInCollectionResponse:
    offset = (page - 1) * limit
    input = GetDocumentsInCollectionInput(
        collection_id=CollectionID.from_value(collection_id),
        search=search,
        limit=limit,
        offset=offset,
        select=select
    )
    result = await get_documents_in_collection_query.execute(input)

    if select:
        return GetDocumentsInCollectionResponse(
            data=[
                {
                    "id": doc.id,
                    "name": doc.name,
                }
                for doc in result.documents
            ],
            meta=None
        )

    import math
    total_pages = math.ceil(result.total / limit)
    has_next_page = page < total_pages
    has_previous_page = page > 1

    return GetDocumentsInCollectionResponse(
        data=[
            {
                "id": doc.id,
                "name": doc.name,
                "filename": doc.filename,
                "status": doc.status,
                "content": doc.content,
                "created_at": doc.created_at
            }
            for doc in result.documents
        ],
        metadata=DocumentsInCollectionMeta(
            page=page,
            limit=limit,
            total=result.total,
            totalPages=total_pages,
            hasNextPage=has_next_page,
            hasPreviousPage=has_previous_page
        )
    )
