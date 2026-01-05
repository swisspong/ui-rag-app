from src.contexts.rag.application.queries.get_collection.get_collection_input import GetCollectionInput
from src.contexts.rag.application.queries.get_collection.get_collection_output import GetCollectionOutput
from src.contexts.rag.application.queries.repoistories.collection_read_repository import CollectionReadRepository


class GetCollectionQuery:
    def __init__(
        self,
        collection_read_repository: CollectionReadRepository
    ):
        self._collection_read_repo = collection_read_repository

    async def execute(self, input: GetCollectionInput) -> GetCollectionOutput:
        collection = await self._collection_read_repo.get_by_id(input.collection_id)
        return GetCollectionOutput(
            collection=collection
        )
