# from src.contexts.collections.domain.service.file_storage import FileStorage
# from src.contexts.collections.domain.entities.file import File
# from src.contexts.collections.domain.value_objects.file_id import FileID
from src.shared.domain.entities.asset import Asset
from src.shared.domain.value_objects.asset_id import AssetID
# from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.shared.domain.repositories.asset_repository import AssetRepository
from src.shared.domain.services.asset_storage import AssetStorage
from src.shared.domain.services.id_generator import IDGenerator
from src.contexts.collections.application.commands.upload_files_for_collection.upload_files_input import UploadFilesInput
# from src.contexts.collections.domain.repositories.file_repository import FileRepository
from src.contexts.collections.application.policies.collection_filename_policy import CollectionFilenamePolicy
from src.contexts.collections.domain.entities.collection_file import CollectionFile
from src.contexts.collections.domain.value_objects.collection_file_id import CollectionFileID

from src.shared.application.errors import (
    UploadFailed
)
from src.shared.infrastructure.errors import (
    FileWriteFailed
)
from src.shared.infrastructure.errors import (
    InfrastructureError,
    DuplicateRecordError,
)
from src.shared.application.errors import (
    DependencyUnavailable
)
from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.contexts.collections.domain.repositories.collection_file_repository import CollectionFileRepository


class UploadFilesHandler:
    def __init__(
        self,
        asset_storage: AssetStorage,
        id_generator: IDGenerator,
        asset_repository: AssetRepository,
        filename_policy: CollectionFilenamePolicy,
        collection_file_repository: CollectionFileRepository
    ):
        self._asset_storage = asset_storage
        self._id_generator = id_generator
        self._asset_repo = asset_repository
        self._filename_policy = filename_policy
        self._collection_file_repo = collection_file_repository

    async def execute(
        self,
        input: UploadFilesInput
    ):
        collection_id = CollectionID.from_value(input.collection_id)
        for f in input.files:
            new_filename = await self._filename_policy.resolve(collection_id, f.filename)
            asset: Asset = Asset.create(
                id=AssetID.from_value(self._id_generator.new_id()),
                filename=new_filename,
                content_type=f.content_type,
                size=f.size,
            )
            collection_file: CollectionFile = CollectionFile.create(
                id=CollectionFileID.from_value(self._id_generator.new_id()),
                collection_id=collection_id,
                asset_id=asset.id
            )
            try:
                await self._asset_storage.save(file=asset, content=f.stream)
            except FileWriteFailed as e:
                raise UploadFailed(
                    f"Upload failed for file {asset.filename}"
                ) from e
            try:
                await self._asset_repo.save(asset)
                await self._collection_file_repo.save(collection_file)
            # except DuplicateRecordError as e:
            #     raise CollectionNameAlreadyExists(name.value) from e
            except InfrastructureError as e:
                print(e)
                raise DependencyUnavailable("Failed to create file") from e
