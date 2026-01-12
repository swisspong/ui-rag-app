from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class AdditionalChunkItem(BaseModel):
    id: str
    content: str
    meta: Dict[str, Any]
    status: str
    version: int
    created_at: Optional[datetime] = Field(..., alias="createdAt", description="ISO 8601 date string when the chunk was created")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "chunk_1",
                "content": "This is an additional chunk content...",
                "meta": {
                    "source": "manual_entry"
                },
                "status": "completed",
                "version": 1,
                "createdAt": "2024-01-15T10:00:00Z"
            }
        }


class AdditionalChunkListMetadata(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int = Field(..., alias="totalPages")
    has_next_page: bool = Field(..., alias="hasNextPage")
    has_previous_page: bool = Field(..., alias="hasPreviousPage")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "page": 1,
                "limit": 10,
                "total": 20,
                "totalPages": 2,
                "hasNextPage": True,
                "hasPreviousPage": False
            }
        }


class GetAdditionalChunksInCollectionResponse(BaseModel):
    data: List[AdditionalChunkItem]
    metadata: AdditionalChunkListMetadata
