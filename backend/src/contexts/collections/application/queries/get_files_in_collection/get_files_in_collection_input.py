from dataclasses import dataclass
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


@dataclass
class GetFilesInCollectionInput:
    """
    Input model for the get_files_in_collection query.
    
    Used to retrieve all files in a collection with asset information.
    """
    collection_id: CollectionID
