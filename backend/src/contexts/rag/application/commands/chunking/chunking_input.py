from dataclasses import dataclass
from typing import List


@dataclass
class ChunkingInput:
    collection_id: str
    document_ids: list[str]
    max_token_size: int = 1024
    overlap_token_size: int = 128
