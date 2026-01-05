from typing import Any, List
from abc import ABC, abstractmethod
from src.contexts.collections.domain.entities.collection import Collection
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


class CollectionRepository(ABC):

    @abstractmethod
    async def save(self, data: Collection, conn: Any = None) -> Collection:
        pass

    # @abstractmethod
    # async def get_by_id(self, id: CollectionID, conn: Any = None) -> List[Collection]:
    #     pass
