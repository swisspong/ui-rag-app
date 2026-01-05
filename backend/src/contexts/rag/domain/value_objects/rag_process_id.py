from dataclasses import dataclass
from src.contexts.collections.domain.errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class RAGProcessID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "RAGProcessID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return RAGProcessID(value)

    @property
    def value(self) -> str:
        return self._value
