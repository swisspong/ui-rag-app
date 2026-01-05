from dataclasses import dataclass
import datetime


@dataclass
class CollectionFileReadModel:
    collection_file_id: str
    filename: str
    size: int
    asset_id: str
    created_at: datetime.datetime
    current_stage: str = 'upload'
    status: str = 'completed'
