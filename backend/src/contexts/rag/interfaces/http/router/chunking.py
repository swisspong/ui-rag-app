
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
    "/{collection_id}/chunking",
    response_model=ChunkingResponse,
    status_code=status.HTTP_200_OK,
    summary="Chunk documents in a collection",
    description="Chunk documents in a collection"
)
@inject
async def chunking(
    collection_id: str,
    request: ChunkingRequest,
    chunking_handler: ChunkingHandler = Depends(
        Provide[ApplicationContainer.rag_package.chunking_handler]),
) -> ChunkingResponse:

    input = ChunkingInput(
        collection_id=collection_id,
        document_ids=request.document_ids,
        max_token_size=request.chunk_size,
        overlap_token_size=request.overlap
    )
    result = await chunking_handler.execute(input)

    return ChunkingResponse()
