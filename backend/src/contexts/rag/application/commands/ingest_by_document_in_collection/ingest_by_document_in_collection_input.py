from dataclasses import dataclass


@dataclass(frozen=True)
class IngestionByDocumentInCollectionInput:
    collection_id: str
    document_id: str
