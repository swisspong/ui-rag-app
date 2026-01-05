from dataclasses import dataclass
from typing import List


@dataclass
class ProcessDocumentInput:
    collection_id: str
    collection_file_ids: List[str]