from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentChunkItem(BaseModel):
    id: str
    version: int
    name: str = Field(..., description="Name of the document")
    chunk_count: int = Field(..., alias="chunkCount", description="Total number of chunks in the document")
    created_at: datetime = Field(..., alias="createdAt", description="ISO 8601 date string when the document was created")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "doc_1",
                "version": 1,
                "name": "Invoice 123",
                "chunkCount": 5,
                "createdAt": "2024-01-15T10:00:00Z"
            }
        }


class DocumentChunkListMetadata(BaseModel):
    offset: int
    limit: int
    total: int
    has_next_page: bool = Field(..., alias="hasNextPage")
    has_previous_page: bool = Field(..., alias="hasPreviousPage")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "offset": 0,
                "limit": 10,
                "total": 20,
                "hasNextPage": True,
                "hasPreviousPage": False
            }
        }


class GetDocumentChunksInCollectionResponse(BaseModel):
    data: List[DocumentChunkItem]
    metadata: DocumentChunkListMetadata
