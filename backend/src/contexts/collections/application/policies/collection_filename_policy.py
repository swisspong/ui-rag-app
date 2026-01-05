from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.repositories.collection_repository import CollectionRepository
from src.contexts.collections.domain.repositories.collection_file_repository import CollectionFileRepository
from src.shared.domain.repositories.asset_repository import AssetRepository


class CollectionFilenamePolicy:
    def __init__(
        self,
        collection_file_repository: CollectionFileRepository,
        asset_repository: AssetRepository
    ):
        self._collection_file_repo = collection_file_repository
        self._asset_repo = asset_repository

    async def resolve(
        self,
        collection_id: CollectionID,
        filename: str
    ) -> str:
        collection_files = await self._collection_file_repo.get_many_by_collection_id(collection_id)
        asset_name = set()
        for collection_file in collection_files:
            asset = await self._asset_repo.get_by_id(collection_file.asset_id)
            asset_name.add(asset.filename)
        if filename not in asset_name:
            return filename
        
        if "." in filename:
            base, ext = filename.rsplit(".", 1)
            ext = "." + ext
        else:
            base, ext = filename, ""

        counter = 1
        while True:
            candidate = f"{base} ({counter}){ext}"
            if candidate not in asset_name:
                return candidate
            counter += 1