from .get_files_in_collection_input import GetFilesInCollectionInput
from ..repositories.collection_read_repository import CollectionReadRepository
from ..models.collection_file_read_model import CollectionFileReadModel


class GetFilesInCollectionQuery:
    def __init__(
        self,
        collection_read_repository: CollectionReadRepository
    ):
        self._collection_read_repo = collection_read_repository

    async def execute(self, input_data: GetFilesInCollectionInput) -> list[CollectionFileReadModel]:
        return await self._collection_read_repo.get_files_in_collection(input_data.collection_id)
