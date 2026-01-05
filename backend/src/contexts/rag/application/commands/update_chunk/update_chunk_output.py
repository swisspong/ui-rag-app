from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class UpdateChunkOutput:
    id: str
    collection_id: str
    document_id: str
    content: str
    meta: Dict[str, Any]
    order_index: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
