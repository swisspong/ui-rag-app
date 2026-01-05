from dataclasses import dataclass
from typing import List


@dataclass
class FailedChunk:
    chunk_id: str
    error_message: str


@dataclass
class IngestMultipleChunksByCollectionOutput:
    success: bool
    ingested_chunk_ids: List[str]
    failed_chunks: List[FailedChunk]
    total_count: int
    ingested_count: int
    failed_count: int
