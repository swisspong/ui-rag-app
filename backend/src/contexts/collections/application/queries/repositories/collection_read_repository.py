from typing import Any, List, Tuple
from abc import ABC, abstractmethod
from src.contexts.collections.domain.value_objects.collection_name import CollectionName
from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.application.queries.models.collection_read_model import CollectionReadModel
from src.contexts.collections.application.queries.models.collection_file_read_model import CollectionFileReadModel
from src.contexts.collections.application.queries.get_collection_list.get_collection_list_input import GetCollectionListInput
from src.contexts.collections.application.queries.get_files_in_collection.get_files_in_collection_input import GetFilesInCollectionInput


class CollectionReadRepository(ABC):
    @abstractmethod
    async def exists_by_name(self, name: CollectionName, conn: Any = None) -> bool:
        pass
        
    @abstractmethod
    async def get_list(self, input_data: GetCollectionListInput, conn: Any = None) -> List[CollectionReadModel]:
        pass
        
    @abstractmethod
    async def get_list_with_count(self, input_data: GetCollectionListInput, conn: Any = None) -> Tuple[List[CollectionReadModel], int]:
        pass
        
    @abstractmethod
    async def get_files_in_collection(self, input_data: GetFilesInCollectionInput, conn: Any = None) -> Tuple[List[CollectionFileReadModel], int]:
        pass
    
    @abstractmethod
    async def get_by_id(self, collection_id: CollectionID, conn: Any = None) -> CollectionReadModel | None:
        pass
