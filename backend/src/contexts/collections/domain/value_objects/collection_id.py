from dataclasses import dataclass
from ..errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class CollectionID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "CollectionID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return CollectionID(value)

    @property
    def value(self) -> str:
        return self._value
