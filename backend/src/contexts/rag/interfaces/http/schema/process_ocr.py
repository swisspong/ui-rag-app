from typing import List
from pydantic import BaseModel


class ProcessOCRRequest(BaseModel):
    collection_file_ids: List[str]


class ProcessOCRResponse(BaseModel):
    success: bool = True
    # message: str = "Collection created successfully"
