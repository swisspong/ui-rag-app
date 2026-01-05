from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_input import GetCollectionFileInCollectionInput

from src.contexts.rag.application.queries.repoistories.collection_file_read_repository import CollectionFileReadRepository


class GetCollectionFileInCollectionQuery:
    def __init__(
        self,
        collection_file_read_repository: CollectionFileReadRepository
    ):
        self._collection_file_read_repo = collection_file_read_repository

    async def execute(self, input: GetCollectionFileInCollectionInput):
        collection_file = await self._collection_file_read_repo.get_by_collection_and_file_id(input.collection_id, input.collection_file_id)
        return collection_file
