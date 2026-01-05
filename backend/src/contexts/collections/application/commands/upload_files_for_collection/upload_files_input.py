
from dataclasses import dataclass
from typing import BinaryIO, List


@dataclass(frozen=True)
class FileItem:
    filename: str
    content_type: str
    size: int
    stream: BinaryIO


@dataclass(frozen=True)
class UploadFilesInput:
    collection_id: str
    files: List[FileItem]
