

import uuid
from typing import Optional

from src.shared.ids.id_generator import IDGenerator

class UUIDIDGenerator(IDGenerator):
    def new_id(self, prefix: Optional[str] = None) -> str:
        uid = uuid.uuid4().hex
        if prefix is None:
            return uid
        p = prefix.strip()
        return f"{p}-{uid}" if p else uid