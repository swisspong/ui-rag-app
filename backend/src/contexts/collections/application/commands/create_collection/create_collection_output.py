from typing import Optional
from dataclasses import dataclass
import datetime




@dataclass(frozen=True)
class CreateCollectionOutput:
    id: str
    name: str
    description: str
    created_at: datetime
