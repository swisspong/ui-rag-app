from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentChunkSummaryReadModel:
    id: str
    version: int
    name: str
    chunk_count: int
    created_at: datetime
