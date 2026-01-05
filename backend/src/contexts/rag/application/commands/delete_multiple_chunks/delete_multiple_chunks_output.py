from dataclasses import dataclass
from typing import List


@dataclass
class DeleteMultipleChunksOutput:
    deleted_chunk_ids: List[str]
    deleted_count: int
