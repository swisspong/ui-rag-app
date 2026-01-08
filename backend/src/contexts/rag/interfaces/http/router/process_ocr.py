
from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.process_ocr import (
    ProcessOCRRequest,
    ProcessOCRResponse
)
from src.contexts.rag.application.commands.process_document.process_document_handler import ProcessDocumentHandler
from src.contexts.rag.application.commands.process_document.process_document_input import ProcessDocumentInput
from src.boot.container import ApplicationContainer
from . import router


@router.post(
    "/{collection_id}/ocr",
    response_model=ProcessOCRResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a list of collections",
    description="Retrieves a paginated list of collections with optional search functionality"
)
@inject
async def process_ocr(
    collection_id: str,
    request: ProcessOCRRequest,
    process_document_handler: ProcessDocumentHandler = Depends(
        Provide[ApplicationContainer.rag_package.process_document_handler]),
) -> ProcessOCRResponse:
    input = ProcessDocumentInput(
        collection_id=collection_id,
        collection_file_ids=request.collection_file_ids
    )
    result = await process_document_handler.execute(input)

    return ProcessOCRResponse()
