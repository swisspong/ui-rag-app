from typing import Any, List
from abc import ABC, abstractmethod

from src.contexts.collections.domain.entities.collection_file import CollectionFile
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


class CollectionFileRepository(ABC):

    @abstractmethod
    async def save(self, data: CollectionFile, conn: Any = None) -> CollectionFile:
        pass

    @abstractmethod
    async def get_many_by_collection_id(self, data: CollectionID, conn: Any = None) -> List[CollectionFile]:
        pass
