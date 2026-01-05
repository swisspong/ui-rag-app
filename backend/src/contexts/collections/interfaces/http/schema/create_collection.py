from typing import Optional
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    model: str = Field(..., description="LLM model identifier")
    base_url: Optional[str] = Field(
        None, description="Base URL for the LLM service")
    api_key: str = Field(..., description="API key for the LLM service")


class EmbeddingConfig(BaseModel):
    model: str = Field(..., description="Embedding model identifier")
    base_url: Optional[str] = Field(None,
                                    description="Base URL for the embedding service")
    api_key: str = Field(..., description="API key for the embedding service")


class ChunkingConfig(BaseModel):
    size: int = Field(
        1200,
        ge=1,
        le=6000,
        description="Optional chunk size for splitting content, default is 1200"
    )
    overlap: int = Field(
        100,
        ge=0,
        le=1000,
        description="Optional overlap size between chunks, default is 100"
    )


class CreateCollectionRequest(BaseModel):
    name: str = Field(..., max_length=50,
                      description="Name of the knowledge (max length 50 characters)")
    description: str = Field(..., max_length=200,
                             description="Detailed description of the knowledge content and purpose (max length 200 characters)")


class CreateCollectionResponse(BaseModel):
    success: bool = True
    message: str = "Collection created successfully"
