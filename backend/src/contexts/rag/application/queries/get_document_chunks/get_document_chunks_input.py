from dataclasses import dataclass
from typing import Optional


@dataclass
class GetDocumentChunksInput:

    collection_id: str
    document_id: str
    version: int
    offset: int
    limit: int
    search: Optional[str] = None
