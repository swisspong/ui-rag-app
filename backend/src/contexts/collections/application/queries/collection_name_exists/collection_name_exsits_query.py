from src.contexts.collections.application.queries.repositories.collection_read_repository import CollectionReadRepository
from src.contexts.collections.domain.value_objects.collection_name import CollectionName


class CollectionNameExistsQuery:
    def __init__(
        self,
        collection_read_repository: CollectionReadRepository
    ):
        self._collection_read_repo = collection_read_repository

    async def execute(self, name: CollectionName) -> bool:
        return await self._collection_read_repo.exists_by_name(name)
