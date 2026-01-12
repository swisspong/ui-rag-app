from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AdditionalChunkReadModel:
    id: str
    content: str
    meta: Dict[str, Any]
    status: str
    version: int
    created_at: datetime
