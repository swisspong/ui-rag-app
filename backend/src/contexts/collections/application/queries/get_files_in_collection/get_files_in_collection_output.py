from dataclasses import dataclass
from typing import List
from ..models.collection_file_read_model import CollectionFileReadModel


@dataclass
class GetFilesInCollectionOutput:
    """
    Output model for the get_files_in_collection query.
    
    Contains the list of files and total count for pagination.
    """
    files: List[CollectionFileReadModel]
    total_count: int
