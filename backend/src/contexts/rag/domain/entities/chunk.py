import datetime
from dataclasses import dataclass
from typing import Optional
from datetime import timezone
from src.contexts.rag.domain.value_objects.doc_chunk_id import DocChunkId

@dataclass
class DocChunk:
    def __init__(
        self,
        *,
        id: DocChunkId,
        workspace: str,
        full_doc_id: str,
        chunk_order_index: int,
        tokens: int,
        content: str,
        file_path: Optional[str],
        create_time: datetime,
        update_time: datetime,
    ):
        self.id = id
        self.workspace = workspace
        self.full_doc_id = full_doc_id
        self.chunk_order_index = chunk_order_index
        self.tokens = tokens
        self.content = content
        self.file_path = file_path
        self.create_time = create_time
        self.update_time = update_time

    @staticmethod
    def create(
        workspace: str,
        full_doc_id: str,
        chunk_order_index: int,
        tokens: int,
        content: str,
        file_path: Optional[str]
    ):
        now = datetime.datetime.now(timezone.utc).replace(tzinfo=None)

        return DocChunk(
            id=DocChunkId.from_content(content),
            workspace=workspace,
            full_doc_id=full_doc_id,
            chunk_order_index=chunk_order_index,
            tokens=tokens,
            content=content,
            file_path=file_path,
            create_time=now,
            update_time=now,
        )
