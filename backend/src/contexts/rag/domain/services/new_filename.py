from abc import ABC, abstractmethod
from src.contexts.rag.domain.value_objects.collection_id import CollectionID


class CollectionFilename(ABC):

    @abstractmethod
    async def resolve(
        self,
        collection_id: CollectionID,
        filename: str,
    ) -> str:
        pass