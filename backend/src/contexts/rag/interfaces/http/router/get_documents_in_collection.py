from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_documents_in_collection import (
    GetDocumentsInCollectionResponse,
    DocumentsInCollectionData,
    DocumentsInCollectionMeta
)
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_query import GetDocumentsInCollectionQuery
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_input import GetDocumentsInCollectionInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/collection/{collection_id}/documents",
    response_model=GetDocumentsInCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get documents in collection",
    description="Retrieves a list of documents in a collection"
)
@inject
async def get_documents_in_collection(
    collection_id: str,
    get_documents_in_collection_query: GetDocumentsInCollectionQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_documents_in_collection_query]),
) -> GetDocumentsInCollectionResponse:
    input = GetDocumentsInCollectionInput(
        collection_id=CollectionID.from_value(collection_id)
    )
    result = await get_documents_in_collection_query.execute(input)

    return GetDocumentsInCollectionResponse(
        data=DocumentsInCollectionData(
            documents=[
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "content": doc.content,
                    "created_at": doc.created_at
                }
                for doc in result.documents
            ]
        ),
        meta=DocumentsInCollectionMeta()
    )
