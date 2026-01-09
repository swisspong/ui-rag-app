from typing import List, Optional
from pydantic import BaseModel, Field


class ChunkMeta(BaseModel):
    page_number: Optional[int] = Field(None, alias="page_number")


class ChunkItem(BaseModel):
    id: str
    content: str
    meta: dict
    status: str


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    totalPages: int
    hasNextPage: bool
    hasPreviousPage: bool


class GetChunksByDocumentIdResponse(BaseModel):
    data: List[ChunkItem]
    metadata: PaginationMeta
