from pathlib import Path
import asyncio
from typing import BinaryIO
from src.contexts.collections.domain.entities.file import File
from src.contexts.collections.domain.value_objects.file_id import FileID
from src.contexts.collections.domain.service.file_storage import FileStorage
from src.shared.infrastructure.errors import (
    FileDeleteFailed,
    FileNotFoundStorageError,
    FileStorageError,
    FileWriteFailed
)


class LocalFileStorage(FileStorage):
    def __init__(self, base_path: str):
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, file_id: FileID) -> Path:
        return self._base_path / file_id.value

    async def save(
        self,
        file: File,
        content: BinaryIO,
    ) -> None:
        path = self._resolve_path(file.id)

        def _write():
            try:
                with open(path, "wb") as f:
                    while chunk := content.read(1024 * 1024):
                        f.write(chunk)
            except Exception as e:
                raise FileWriteFailed(
                    f"Failed to write file {file.id.value}"
                ) from e

        await asyncio.to_thread(_write)

    async def open(
        self,
        file_id: FileID,
    ) -> BinaryIO:
        path = self._resolve_path(file_id)
        if not path.exists():
            raise FileNotFoundStorageError(
                f"File {file_id.value} not found"
            )
        try:
            return open(path, "rb")
        except Exception as e:
            raise FileStorageError(
                f"Failed to open file {file_id.value}"
            ) from e

    async def delete(
        self,
        file_id: FileID,
    ) -> None:
        path = self._resolve_path(file_id)

        try:
            if path.exists():
                await asyncio.to_thread(path.unlink)
        except Exception as e:
            raise FileDeleteFailed(
                f"Failed to delete file {file_id.value}"
            ) from e
