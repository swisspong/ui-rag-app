from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentItem(BaseModel):
    id: str
    name: str
    filename: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "123",
                "name": "My Doc",
                "filename": "doc.pdf",
                "status": "completed",
                "content": "...",
                "createdAt": "2024-01-01T00:00:00Z"
            }
        }


class DocumentsInCollectionMeta(BaseModel):
    page: int
    limit: int
    total: int
    totalPages: int
    hasNextPage: bool
    hasPreviousPage: bool


class GetDocumentsInCollectionResponse(BaseModel):
    data: List[DocumentItem] = Field(
        ..., description="Data containing the list of documents")
    metadata: Optional[DocumentsInCollectionMeta] = Field(None,
                                                      description="Metadata about the response")
