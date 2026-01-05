from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionDescription:
    _value: str

    @staticmethod
    def from_value(value: str) -> "CollectionDescription":
        return CollectionDescription(value.strip())

    @property
    def value(self) -> str:
        return self._value
