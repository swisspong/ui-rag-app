from typing import List
from pydantic import BaseModel, Field


class IngestMultipleChunksByCollectionRequest(BaseModel):
    chunk_ids: List[str] = Field(..., description="List of chunk IDs to ingest")


class FailedChunkResponse(BaseModel):
    chunk_id: str = Field(..., description="ID of the chunk that failed to ingest")
    error_message: str = Field(..., description="Error message describing why the chunk failed")


class IngestMultipleChunksByCollectionData(BaseModel):
    success: bool = Field(..., description="Whether the overall operation was successful")
    ingested_chunk_ids: List[str] = Field(..., description="List of chunk IDs that were successfully ingested")
    failed_chunks: List[FailedChunkResponse] = Field(..., description="List of chunks that failed to ingest with error details")
    total_count: int = Field(..., description="Total number of chunks requested to be ingested")
    ingested_count: int = Field(..., description="Number of chunks successfully ingested")
    failed_count: int = Field(..., description="Number of chunks that failed to ingest")


class IngestMultipleChunksByCollectionMeta(BaseModel):
    pass


class IngestMultipleChunksByCollectionResponse(BaseModel):
    data: IngestMultipleChunksByCollectionData = Field(..., description="Data containing ingestion results")
    meta: IngestMultipleChunksByCollectionMeta = Field(..., description="Metadata about the response")
