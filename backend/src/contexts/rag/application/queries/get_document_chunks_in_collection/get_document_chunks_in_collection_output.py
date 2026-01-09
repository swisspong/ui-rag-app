from dataclasses import dataclass
from typing import List
from src.contexts.rag.application.queries.models.document_chunk_summary_read_model import DocumentChunkSummaryReadModel


@dataclass
class GetDocumentChunksInCollectionOutput:
    data: List[DocumentChunkSummaryReadModel]
    total: int
    offset: int
    limit: int
