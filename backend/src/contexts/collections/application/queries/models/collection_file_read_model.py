from dataclasses import dataclass
import datetime


@dataclass
class CollectionFileReadModel:
    id: str
    filename: str
    size: int | None = None
    type: str | None = None
    created_at: datetime.datetime | None = None
