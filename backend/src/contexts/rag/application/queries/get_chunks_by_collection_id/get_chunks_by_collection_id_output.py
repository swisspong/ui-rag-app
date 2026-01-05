from dataclasses import dataclass
from typing import List
from src.contexts.rag.application.queries.models.chunk_read_model import ChunkReadModel


@dataclass
class GetChunksByCollectionIdOutput:
    chunks: List[ChunkReadModel]
