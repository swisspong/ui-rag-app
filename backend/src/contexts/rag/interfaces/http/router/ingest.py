
from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.ingest import (
    IngestRequest,
    IngestResponse
)
from src.contexts.rag.application.commands.ingest_by_document_in_collection.ingest_by_document_in_collection_handler import IngestByDocumentInCollectionHandler
from src.contexts.rag.application.commands.ingest_by_document_in_collection.ingest_by_document_in_collection_input import IngestionByDocumentInCollectionInput
from src.boot.container import ApplicationContainer
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
    ingest_by_document_in_collection_handler: IngestByDocumentInCollectionHandler = Depends(
        Provide[ApplicationContainer.rag_package.ingest_by_document_in_collection_handler]),
) -> IngestResponse:
    input = IngestionByDocumentInCollectionInput(
        collection_id=request.collection_id,
        document_id=request.document_id
    )
    result = await ingest_by_document_in_collection_handler.execute(input)

    return IngestResponse()
