from dataclasses import dataclass
from typing import Optional


@dataclass
class GetAdditionalChunksInput:
    collection_id: str
    page: int = 1
    limit: int = 10
    search: Optional[str] = None
