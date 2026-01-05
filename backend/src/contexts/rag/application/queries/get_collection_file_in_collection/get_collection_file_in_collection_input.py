from dataclasses import dataclass


@dataclass
class GetCollectionFileInCollectionInput:
    collection_id: str
    collection_file_id: str
