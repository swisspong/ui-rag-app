from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ChunkReadModel:
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: dict
    order_index: int
    process_status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
