from typing import List
from pydantic import BaseModel, Field


class ChunkingRequest(BaseModel):
    collection_id: str
    document_ids: List[str]
    chunk_size: int = Field(1024)
    overlap: int = Field(100)


class ChunkingResponse(BaseModel):
    success: bool = True
    # message: str = "Collection created successfully"
