from dataclasses import dataclass
from src.contexts.collections.domain.errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class ChunkID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "ChunkID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return ChunkID(value)

    @property
    def value(self) -> str:
        return self._value
