from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ChunkByIdAndCollectionIdItem(BaseModel):
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: dict
    order_index: int
    process_status: str
    created_at: datetime
    updated_at: datetime


class ChunkByIdAndCollectionIdData(BaseModel):
    chunk: Optional[ChunkByIdAndCollectionIdItem] = Field(None, description="Chunk details")


class ChunkByIdAndCollectionIdMeta(BaseModel):
    pass


class GetChunkByIdAndCollectionIdResponse(BaseModel):
    data: ChunkByIdAndCollectionIdData = Field(..., description="Data containing the chunk")
    meta: ChunkByIdAndCollectionIdMeta = Field(..., description="Metadata about the response")
