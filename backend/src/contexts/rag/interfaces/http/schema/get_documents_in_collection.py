from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentItem(BaseModel):
    id: str
    name: str
    filename: str
    status: str = "pending"
    content: str
    created_at: datetime = Field(..., alias="createdAt")

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
    meta: DocumentsInCollectionMeta = Field(...,
                                            description="Metadata about the response")
