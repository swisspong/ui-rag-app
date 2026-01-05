from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class CollectionFileResponse(BaseModel):
    collection_file_id: str = Field(..., description="Unique identifier for the collection file")
    filename: str = Field(..., description="Name of the file")
    size: int = Field(..., description="Size of the file in bytes")
    asset_id: str = Field(..., description="Asset identifier for the file")
    created_at: datetime = Field(..., description="Timestamp when the file was created")
    current_stage: str = 'upload'
    status: str = 'completed'


class DataWrapper(BaseModel):
    files: List[CollectionFileResponse] = Field(..., description="List of files in the collection")


class GetFilesInCollectionResponse(BaseModel):
    data: DataWrapper = Field(..., description="Data wrapper containing files")
