from dataclasses import dataclass
from typing import Optional
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


@dataclass
class GetFilesInCollectionInput:
    """
    Input model for the get_files_in_collection query.
    
    Used to retrieve a paginated list of files in a collection with optional filtering.
    """
    collection_id: CollectionID
    search: Optional[str] = None
    order_by: str = "created_at"
    limit: int = 20
    offset: int = 0
