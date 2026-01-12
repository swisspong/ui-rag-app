from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentItem(BaseModel):
    id: str
    filename: str
    content: str
    created_at: datetime


class DocumentByCollectionAndFileIdData(BaseModel):
    document: Optional[DocumentItem] = Field(None, description="Document details")


class DocumentByCollectionAndFileIdMeta(BaseModel):
    pass


class GetDocumentByCollectionAndFileIdResponse(BaseModel):
    data: DocumentByCollectionAndFileIdData = Field(..., description="Data containing the document")
    metadata: DocumentByCollectionAndFileIdMeta = Field(..., description="Metadata about the response")
