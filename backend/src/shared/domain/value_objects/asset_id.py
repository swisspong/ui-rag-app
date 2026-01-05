from dataclasses import dataclass

from src.contexts.collections.domain.errors.invalid_file_id import InvalidFileId

@dataclass(frozen=True)
class AssetID:
    _value: str

    @staticmethod
    def from_value(value: str) -> "AssetID":
        if not value or not value.strip():
            raise InvalidFileId()

        return AssetID(value)

    @property
    def value(self) -> str:
        return self._value
