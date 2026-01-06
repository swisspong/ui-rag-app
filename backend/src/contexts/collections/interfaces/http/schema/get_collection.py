from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CollectionData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    id: str = Field(..., description="Unique identifier for the collection")
    name: str = Field(..., description="Name of the collection")
    description: str = Field(..., description="Description of the collection")
    file_count: int = Field(..., description="Number of files in the collection")
    created_at: datetime = Field(..., description="Timestamp when the collection was created")


class GetCollectionResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    data: CollectionData = Field(..., description="Data containing the collection details")
    message: str = Field(..., description="Response message")
