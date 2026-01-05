from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionName:
    _value: str

    @staticmethod
    def from_value(value: str) -> "CollectionName":
        return CollectionName(value.strip())

    @property
    def value(self) -> str:
        return self._value
