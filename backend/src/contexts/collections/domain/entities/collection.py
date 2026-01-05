from dataclasses import dataclass
import datetime
from datetime import timezone

from ..value_objects.collection_id import CollectionID
from ..value_objects.collection_name import CollectionName
from ..value_objects.collection_description import CollectionDescription
from .....shared.domain.services.id_generator import IDGenerator


@dataclass
class Collection:
    id: CollectionID
    name: CollectionName
    description: CollectionDescription
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: IDGenerator,
        name: CollectionName,
        description: CollectionDescription,
    ) -> "Collection":

        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return Collection(
            id=CollectionID.from_value(id.new_id()),
            name=name,
            description=description,
            created_at=now,
            updated_at=now
        )
