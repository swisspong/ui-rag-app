from dataclasses import dataclass
from typing import List
from src.contexts.rag.application.queries.models.document_chunk_read_model import DocumentChunkReadModel


@dataclass
class GetDocumentChunksOutput:

    data: List[DocumentChunkReadModel]
    total: int
