from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DocumentName:
    _value: str

    def __post_init__(self):
        if not self._value:
            raise ValueError("Document name cannot be empty")

    @classmethod
    def from_value(cls, value: Any) -> "DocumentName":
        if not isinstance(value, str):
            raise ValueError("Document name must be a string")
        return cls(_value=value)

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value
