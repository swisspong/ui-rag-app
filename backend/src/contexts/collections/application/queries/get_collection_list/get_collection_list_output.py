from dataclasses import dataclass
from typing import List
from src.contexts.collections.application.queries.models.collection_read_model import CollectionReadModel


@dataclass
class GetCollectionListOutput:
    """
    Output model for the get_collection_list query.
    
    Contains the list of collections and the total count for pagination.
    """
    collections: List[CollectionReadModel]
    total_count: int