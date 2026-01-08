from dataclasses import dataclass
import datetime


@dataclass
class DocumentReadModel:
    id: str
    collection_file_id: str
    name: str
    filename: str
    status: str
    content: str
    created_at: datetime.datetime
