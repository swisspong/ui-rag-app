from dataclasses import dataclass
from src.contexts.rag.application.queries.models.collection_read_model import CollectionReadModel


@dataclass
class GetCollectionOutput:
    collection: CollectionReadModel
