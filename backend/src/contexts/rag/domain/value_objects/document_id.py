from dataclasses import dataclass
from src.contexts.collections.domain.errors.invalid_collection_id import InvalidCollectionId


@dataclass(frozen=True)
class DocumentID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "DocumentID":
        if not value or not value.strip():
            raise InvalidCollectionId()

        return DocumentID(value)

    @property
    def value(self) -> str:
        return self._value
