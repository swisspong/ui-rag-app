
from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.chunking import (
    ChunkingRequest,
    ChunkingResponse
)
from src.contexts.rag.application.commands.chunking.chunking_handler import ChunkingHandler
from src.contexts.rag.application.commands.chunking.chunking_input import ChunkingInput
from src.boot.container import ApplicationContainer
from . import router


@router.post(
    "/chunk",
    response_model=ChunkingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a list of collections",
    description="Retrieves a paginated list of collections with optional search functionality"
)
@inject
async def chunking(
    request: ChunkingRequest,
    chunking_handler: ChunkingHandler = Depends(
        Provide[ApplicationContainer.rag_package.chunking_handler]),
) -> ChunkingResponse:
    input = ChunkingInput(
        collection_id=request.collection_id,
        document_ids=request.document_ids,
        max_token_size=request.chunk_size,
        overlap_token_size=request.overlap
    )
    result = await chunking_handler.execute(input)

    return ChunkingResponse()
