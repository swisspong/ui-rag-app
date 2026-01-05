from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentItem(BaseModel):
    id: str
    filename: str
    content: str
    created_at: datetime


class DocumentsInCollectionData(BaseModel):
    documents: List[DocumentItem] = Field(..., description="List of documents")


class DocumentsInCollectionMeta(BaseModel):
    pass


class GetDocumentsInCollectionResponse(BaseModel):
    data: DocumentsInCollectionData = Field(..., description="Data containing the list of documents")
    meta: DocumentsInCollectionMeta = Field(..., description="Metadata about the response")
