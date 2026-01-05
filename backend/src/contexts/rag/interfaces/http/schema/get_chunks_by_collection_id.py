from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ChunkByCollectionIdItem(BaseModel):
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: dict
    order_index: int
    process_status: str
    created_at: datetime
    updated_at: datetime


class ChunksByCollectionIdData(BaseModel):
    chunks: List[ChunkByCollectionIdItem] = Field(..., description="List of chunks in the collection")


class ChunksByCollectionIdMeta(BaseModel):
    pass


class GetChunksByCollectionIdResponse(BaseModel):
    data: ChunksByCollectionIdData = Field(..., description="Data containing the chunks")
    meta: ChunksByCollectionIdMeta = Field(..., description="Metadata about the response")
