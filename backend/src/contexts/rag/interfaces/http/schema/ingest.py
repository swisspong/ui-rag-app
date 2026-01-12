from pydantic import BaseModel


from typing import Literal

class IngestRequest(BaseModel):
    document_id: str
    collection_id: str
    version: int
    status: Literal["pending", "failed"]


class IngestResponse(BaseModel):
    success: bool = True
