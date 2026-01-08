from dataclasses import dataclass
from typing import Optional
import datetime


@dataclass
class DocumentReadModel:
    id: str
    name: str
    collection_file_id: Optional[str] = None
    filename: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
