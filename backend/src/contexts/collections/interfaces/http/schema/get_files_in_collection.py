from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CollectionFileResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    id: str = Field(..., description="Unique identifier for the collection file")
    name: str = Field(..., description="Name of the file")
    size: Optional[int] = Field(None, description="Size of the file in bytes")
    type: Optional[str] = Field(None, description="Type of the file")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the file was created")


class FilesListMeta(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    total: int = Field(
        ..., description="Total number of files available")
    limit: int = Field(...,
                       description="Maximum number of files returned in this response")
    page: int = Field(...,
                      description="Current page number")
    total_pages: int = Field(..., description="Total number of pages")
    search: Optional[str] = Field(
        None, description="Search term used to filter files")
    has_next_page: bool
    has_previous_page: bool


class GetFilesInCollectionResponse(BaseModel):
    data: List[CollectionFileResponse] = Field(...,
                                               description="Data containing the list of files")
    metadata: Optional[FilesListMeta] = Field(None,
                                              description="Metadata about the pagination and search")
