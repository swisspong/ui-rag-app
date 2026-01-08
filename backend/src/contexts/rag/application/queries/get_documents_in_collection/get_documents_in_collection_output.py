from dataclasses import dataclass
from typing import List
from src.contexts.rag.application.queries.models.document_read_model import DocumentReadModel


@dataclass
class GetDocumentsInCollectionOutput:
    documents: List[DocumentReadModel]
    total: int
