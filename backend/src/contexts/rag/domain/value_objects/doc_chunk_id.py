
from src.contexts.rag.domain.utils.hashing import compute_args_hash


class DocChunkId:
    __slots__ = ("_value",)

    def __init__(self, value: str):
        if not value:
            raise ValueError("DocChunkId cannot be empty")
        self._value = value

    @staticmethod
    def from_content(content: str):
        prefix = "chunk-"
        raw = compute_args_hash(content)
        return DocChunkId(prefix + raw)

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other):
        return isinstance(other, DocChunkId) and self._value == other._value
