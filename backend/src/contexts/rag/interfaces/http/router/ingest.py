
from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.ingest import (
    IngestRequest,
    IngestResponse
)
from src.contexts.rag.application.commands.embed_by_document_in_collection.embed_by_document_in_collection_handler import EmbedByDocumentInCollectionHandler
from src.contexts.rag.application.commands.embed_by_document_in_collection.embed_by_document_in_collection_input import EmbedByDocumentInCollectionInput
from src.boot.container import ApplicationContainer
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.stage_execution import ProcessStatus
from . import router


@router.post(
    "/ingest",
    response_model=IngestResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest a document into a collection",
    description="Ingests a document into a collection for RAG processing"
)
@inject
async def ingest(
    request: IngestRequest,
    embed_by_document_in_collection_handler: EmbedByDocumentInCollectionHandler = Depends(
        Provide[ApplicationContainer.rag_package.embed_by_document_in_collection_handler]),
) -> IngestResponse:

    input = EmbedByDocumentInCollectionInput(
        collection_id=CollectionID.from_value(request.collection_id),
        document_id=DocumentID.from_value(request.document_id),
        version=request.version,
        status=ProcessStatus(request.status)
    )
    result = await embed_by_document_in_collection_handler.execute(input)

    return IngestResponse()
