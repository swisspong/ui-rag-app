from dataclasses import dataclass

from src.contexts.collections.domain.value_objects.file_id import FileID
from src.contexts.collections.domain.value_objects.collection_id import CollectionID


@dataclass
class File:
    id: FileID
    collection_id: CollectionID
    filename: str
    content_type: str
    size: int

    @staticmethod
    def create(
        id: FileID,
        collection_id: CollectionID,
        filename: str,
        content_type: str,
        size: int,
    ) -> "File":
        return File(
            id=id,
            collection_id=collection_id,
            filename=filename,
            content_type=content_type,
            size=size
        )

    # def mark_processing(self):
    #     if self.status != FileStatus.UPLOADED:
    #         raise ValueError("File is not in UPLOADED state")
    #     self.status = FileStatus.PROCESSING

    # def mark_processed(self):
    #     self.status = FileStatus.PROCESSED

    # def mark_failed(self):
    #     self.status = FileStatus.FAILED
