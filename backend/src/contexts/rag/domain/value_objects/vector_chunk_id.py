from dataclasses import dataclass
from src.contexts.collections.domain.errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class VectorChunkID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "VectorChunkID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return VectorChunkID(value)

    @property
    def value(self) -> str:
        return self._value
