from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class UpdateChunkRequest(BaseModel):
    content: str = Field(..., description="The updated content of the chunk")
    meta: Optional[Dict[str, Any]] = Field(None, description="Optional metadata for the chunk")


class UpdateChunkItem(BaseModel):
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: Dict[str, Any]
    order_index: int
    created_at: datetime
    updated_at: datetime


class UpdateChunkData(BaseModel):
    chunk: Optional[UpdateChunkItem] = Field(None, description="Updated chunk details")


class UpdateChunkMeta(BaseModel):
    pass


class UpdateChunkResponse(BaseModel):
    data: UpdateChunkData = Field(..., description="Data containing the updated chunk")
    meta: UpdateChunkMeta = Field(..., description="Metadata about the response")
