from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.get_document_by_collection_and_file_id import (
    GetDocumentByCollectionAndFileIdResponse,
    DocumentByCollectionAndFileIdData,
    DocumentByCollectionAndFileIdMeta
)
from src.contexts.rag.application.queries.get_document_by_collection_and_file_id.get_document_by_collection_and_file_id_query import GetDocumentByCollectionAndFileIdQuery
from src.contexts.rag.application.queries.get_document_by_collection_and_file_id.get_document_by_collection_and_file_id_input import GetDocumentByCollectionAndFileIdInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.boot.container import ApplicationContainer
from . import router


@router.get(
    "/collection/{collection_id}/files/{collection_file_id}/document",
    response_model=GetDocumentByCollectionAndFileIdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get document by collection and file id",
    description="Retrieves a single document in a collection by collection_id and collection_file_id"
)
@inject
async def get_document_by_collection_and_file_id(
    collection_id: str,
    collection_file_id: str,
    get_document_by_collection_and_file_id_query: GetDocumentByCollectionAndFileIdQuery = Depends(
        Provide[ApplicationContainer.rag_package.get_document_by_collection_and_file_id_query]),
) -> GetDocumentByCollectionAndFileIdResponse:
    input = GetDocumentByCollectionAndFileIdInput(
        collection_id=CollectionID.from_value(collection_id),
        collection_file_id=CollectionFileID.from_value(collection_file_id)
    )
    result = await get_document_by_collection_and_file_id_query.execute(input)

    document_data = None
    if result is not None:
        document_data = {
            "id": result.id,
            "filename": result.filename,
            "content": result.content,
            "created_at": result.created_at
        }

    return GetDocumentByCollectionAndFileIdResponse(
        data=DocumentByCollectionAndFileIdData(
            document=document_data
        ),
        metadata=DocumentByCollectionAndFileIdMeta()
    )
