from dataclasses import dataclass
from typing import Optional
from src.contexts.collections.application.queries.models.collection_read_model import CollectionReadModel


@dataclass
class GetCollectionOutput:
    """
    Output model for the get_collection query.
    
    Contains the collection data or None if not found.
    """
    collection: Optional[CollectionReadModel]
