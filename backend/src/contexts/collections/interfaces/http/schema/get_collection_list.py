from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CollectionResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    id: str = Field(..., description="Unique identifier for the collection")
    name: str = Field(..., description="Name of the collection")
    description: str = Field(..., description="Description of the collection")
    file_count: int
    created_at: datetime = Field(...,
                                 description="Timestamp when the collection was created")
    updated_at: datetime = Field(...,
                                 description="Timestamp when the collection was last updated")


class GetCollectionListRequest(BaseModel):
    search: Optional[str] = Field(
        None, description="Search term to filter collections by name or description")
    order_by: str = Field(
        "created_at", description="Field to order the results by (e.g., created_at, updated_at, name)")
    limit: int = Field(
        20, ge=1, le=100, description="Maximum number of collections to return")
    page: int = Field(
        1, ge=1, description="Number of collections to skip for pagination")


class CollectionListData(BaseModel):
    collections: List[CollectionResponse] = Field(
        ..., description="List of collections matching the query")


class CollectionListMeta(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    total: int = Field(
        ..., description="Total number of collections available")
    limit: int = Field(...,
                       description="Maximum number of collections returned in this response")
    page: int = Field(...,
                      description="Number of collections skipped for pagination")
    total_pages: int = Field(..., description="")
    search: Optional[str] = Field(
        None, description="Search term used to filter collections")
    has_next_page: bool
    has_previous_page: bool


class GetCollectionListResponse(BaseModel):

    data: CollectionListData = Field(...,
                                     description="Data containing the list of collections")
    meta: CollectionListMeta = Field(...,
                                     description="Metadata about the pagination and search")
