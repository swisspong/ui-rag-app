from typing import List
from src.contexts.rag.domain.entities.chunk import DocChunk
from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.infrastructure.sql.doc_chunk import UPSERT_TEXT_CHUNK
from src.contexts.rag.domain.repositories.kv_repoisory import KVRepository


class PGKVRepository(KVRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def upsert_text_chunk(self, data: List[DocChunk], conn=None) -> None:
        for chunk in data:
            await self._db.execute(
                UPSERT_TEXT_CHUNK,
                chunk.workspace,
                chunk.id,
                chunk.tokens,
                chunk.chunk_order_index,
                chunk.full_doc_id,
                chunk.content,
                chunk.file_path,
                [],
                chunk.create_time,
                chunk.update_time,
                conn=conn,
            )
