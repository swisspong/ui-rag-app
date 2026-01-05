from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class CollectionFileReadModel:
    id: str
    collection_id: str
    asset_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
