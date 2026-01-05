import datetime
from typing import Optional, List
from datetime import timezone

from api.src.contexts.rag.domain.value_objects.doc_chunk_id import DocChunkId


class VectorChunk:
    def __init__(
        self,
        *,
        id: DocChunkId,
        vector: List[float],
        full_doc_id: str,
        content: str,
        file_path: Optional[str],
        create_at: int,
    ):
        self.id = id
        self.vector = vector
        self.full_doc_id = full_doc_id
        self.content = content
        self.file_path = file_path
        self.create_at = create_at

    @staticmethod
    def create(
        id: DocChunkId,
        vector: List[float],
        full_doc_id: str,
        content: str,
        file_path: Optional[str]
    ):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return VectorChunk(
            id=id,
            vector=vector,
            full_doc_id=full_doc_id,
            content=content,
            file_path=file_path,
            create_at=now
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id.value,        # สำคัญ: แปลง VO
            "vector": self.vector,
            "full_doc_id": self.full_doc_id,
            "content": self.content,
            "file_path": self.file_path,
            "create_at": self.create_at,
        }
