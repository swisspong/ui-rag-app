from abc import ABC, abstractmethod
from typing import BinaryIO
from src.contexts.collections.domain.entities.file import File


class FileStorage(ABC):
    @abstractmethod
    async def save(
        self,
        *,
        file: File,
        content: BinaryIO,
    ) -> None:
        pass
