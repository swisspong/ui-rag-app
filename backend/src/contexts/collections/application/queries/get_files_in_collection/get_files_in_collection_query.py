from .get_files_in_collection_input import GetFilesInCollectionInput
from .get_files_in_collection_output import GetFilesInCollectionOutput
from ..repositories.collection_read_repository import CollectionReadRepository


class GetFilesInCollectionQuery:
    def __init__(
        self,
        collection_read_repository: CollectionReadRepository
    ):
        self._collection_read_repo = collection_read_repository

    async def execute(self, input_data: GetFilesInCollectionInput) -> GetFilesInCollectionOutput:
        files, total_count = await self._collection_read_repo.get_files_in_collection(input_data)
        return GetFilesInCollectionOutput(files=files, total_count=total_count)
