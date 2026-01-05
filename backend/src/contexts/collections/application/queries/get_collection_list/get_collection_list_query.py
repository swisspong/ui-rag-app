from .get_collection_list_input import GetCollectionListInput
from .get_collection_list_output import GetCollectionListOutput
from ..repositories.collection_read_repository import CollectionReadRepository


class GetCollectionListQuery:
    def __init__(
        self,
        collection_read_repository: CollectionReadRepository
    ):
        self._collection_read_repo = collection_read_repository

    async def execute(self, input_data: GetCollectionListInput) -> GetCollectionListOutput:
        collections, total_count = await self._collection_read_repo.get_list_with_count(input_data)
        return GetCollectionListOutput(
            collections=collections,
            total_count=total_count
        )