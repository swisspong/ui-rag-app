from typing import List
from pydantic import BaseModel, Field


class DeleteMultipleChunksMeta(BaseModel):
    pass


class DeleteMultipleChunksData(BaseModel):
    deleted_chunk_ids: List[str] = Field(..., description="List of chunk IDs that were requested to be deleted")
    deleted_count: int = Field(..., description="Number of chunks actually deleted from the database")


class DeleteMultipleChunksResponse(BaseModel):
    data: DeleteMultipleChunksData = Field(..., description="Data containing deletion results")
    meta: DeleteMultipleChunksMeta = Field(..., description="Metadata about the response")
