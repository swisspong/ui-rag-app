from pydantic import BaseModel


class IngestRequest(BaseModel):
    document_id: str
    collection_id: str


class IngestResponse(BaseModel):
    success: bool = True
