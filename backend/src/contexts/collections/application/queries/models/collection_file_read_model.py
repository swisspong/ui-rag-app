from dataclasses import dataclass
import datetime


@dataclass
class CollectionFileReadModel:
    id: str
    filename: str
    size: int
    type: str
    created_at: datetime.datetime
