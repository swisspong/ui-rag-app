from dataclasses import dataclass
import datetime
from datetime import timezone

from ..value_objects.collection_id import CollectionID
from src.shared.domain.value_objects.asset_id import AssetID
from ..value_objects.collection_file_id import CollectionFileID


@dataclass
class CollectionFile:
    id: CollectionFileID
    collection_id: CollectionID
    asset_id: AssetID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: CollectionFileID,
        collection_id: CollectionID,
        asset_id: AssetID,
    ) -> "CollectionFile":

        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return CollectionFile(
            id=id,
            collection_id=collection_id,
            asset_id=asset_id,
            created_at=now,
            updated_at=now
        )
