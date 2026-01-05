from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.rag.interfaces.http.schema.ingest_multiple_chunks_by_collection import (
    IngestMultipleChunksByCollectionResponse,
    IngestMultipleChunksByCollectionData,
    IngestMultipleChunksByCollectionMeta,
    FailedChunkResponse,
    IngestMultipleChunksByCollectionRequest
)
from src.contexts.rag.application.commands.ingest_multiple_chunks_by_collection.ingest_multiple_chunks_by_collection_handler import IngestMultipleChunksByCollectionHandler
from src.contexts.rag.application.commands.ingest_multiple_chunks_by_collection.ingest_multiple_chunks_by_collection_input import IngestMultipleChunksByCollectionInput
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.boot.container import ApplicationContainer
from . import router


@router.post(
    "/collections/{collection_id}/chunks/ingest",
    response_model=IngestMultipleChunksByCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest multiple chunks by collection ID and chunk IDs",
    description="Ingests multiple chunks in a collection by collection_id and a list of chunk_ids"
)
@inject
async def ingest_multiple_chunks_by_collection(
    collection_id: str,
    request: IngestMultipleChunksByCollectionRequest,
    ingest_multiple_chunks_by_collection_handler: IngestMultipleChunksByCollectionHandler = Depends(
        Provide[ApplicationContainer.rag_package.ingest_multiple_chunks_by_collection_handler]),
) -> IngestMultipleChunksByCollectionResponse:
    input = IngestMultipleChunksByCollectionInput(
        collection_id=CollectionID.from_value(collection_id),
        chunk_ids=[ChunkID.from_value(chunk_id) for chunk_id in request.chunk_ids]
    )
    result = await ingest_multiple_chunks_by_collection_handler.execute(input)

    failed_chunks_response = [
        FailedChunkResponse(
            chunk_id=failed_chunk.chunk_id,
            error_message=failed_chunk.error_message
        )
        for failed_chunk in result.failed_chunks
    ]

    return IngestMultipleChunksByCollectionResponse(
        data=IngestMultipleChunksByCollectionData(
            success=result.success,
            ingested_chunk_ids=result.ingested_chunk_ids,
            failed_chunks=failed_chunks_response,
            total_count=result.total_count,
            ingested_count=result.ingested_count,
            failed_count=result.failed_count
        ),
        meta=IngestMultipleChunksByCollectionMeta()
    )
