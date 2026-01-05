from typing import Any
from abc import ABC, abstractmethod
from src.contexts.collections.domain.entities.file import File


class FileRepository(ABC):

    @abstractmethod
    async def save(self, data: File, conn: Any = None) -> File:
        pass
