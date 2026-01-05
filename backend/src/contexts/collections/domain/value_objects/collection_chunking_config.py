from dataclasses import dataclass
from ..errors.invalid_chunking_config import InvalidChunkingConfig


@dataclass(frozen=True)
class CollectionChunkingConfig:
    _size: int
    _overlap: int

    @staticmethod
    def from_value(size: int, overlap: int):
        if size <= 0:
            raise InvalidChunkingConfig(
                size, overlap, "chunk_size must be greater than 0"
            )

        if overlap < 0:
            raise InvalidChunkingConfig(
                size, overlap, "chunk_overlap cannot be negative"
            )

        if overlap >= size:
            raise InvalidChunkingConfig(
                size, overlap, "chunk_overlap must be less than chunk_size"
            )

        return CollectionChunkingConfig(size, overlap)

    @property
    def size(self) -> int:
        return self._size

    @property
    def overlap(self) -> int:
        return self._overlap
