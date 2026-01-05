from dataclasses import dataclass
import datetime


@dataclass
class DocumentReadModel:
    id: str
    collection_file_id: str
    filename: str
    content: str
    created_at: datetime.datetime
