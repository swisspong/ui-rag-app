from dataclasses import dataclass
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


@dataclass
class GetCollectionInput:
    """
    Input model for the get_collection query.
    
    Used to retrieve a single collection by its ID.
    """
    collection_id: CollectionID
