from typing import List, Dict
from pydantic import BaseModel, Field


class ChunkItem(BaseModel):
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: Dict
    process_status: str


class ChunksByCollectionFileIdData(BaseModel):
    chunks: List[ChunkItem] = Field(..., description="List of chunks")


class ChunksByCollectionFileIdMeta(BaseModel):
    pass


class GetChunksByCollectionFileIdResponse(BaseModel):
    data: ChunksByCollectionFileIdData = Field(..., description="Data containing the list of chunks")
    meta: ChunksByCollectionFileIdMeta = Field(..., description="Metadata about the response")
