from dataclasses import dataclass
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID


@dataclass
class GetDocumentByCollectionAndFileIdInput:
    collection_id: CollectionID
    collection_file_id: CollectionFileID
