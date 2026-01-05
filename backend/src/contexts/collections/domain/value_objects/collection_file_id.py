from dataclasses import dataclass
from ..errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class CollectionFileID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "CollectionFileID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return CollectionFileID(value)

    @property
    def value(self) -> str:
        return self._value
