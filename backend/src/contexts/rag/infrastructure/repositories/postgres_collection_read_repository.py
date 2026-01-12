from typing import Any
import json

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.contexts.rag.application.queries.repoistories.collection_read_repository import CollectionReadRepository
from src.contexts.rag.application.queries.models.collection_read_model import (
    CollectionReadModel,
    LLMConfigReadModel,
    EmbeddingConfigReadModel,
    ChunkingConfigReadModel
)
from src.contexts.rag.infrastructure.sql.get_collection_by_id import GET_COLLECTION_BY_ID
from src.shared.infrastructure.errors import QueryFailed, DatabaseError


class PostgresCollectionReadRepository(CollectionReadRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def get_by_id(self, id: str, conn: Any = None) -> CollectionReadModel:
        try:
            row = await self._db.fetchrow(
                GET_COLLECTION_BY_ID,
                id,
                conn=conn,
            )
            if row is None:
                raise ValueError(f"Collection with id {id} not found")
            
            chunking_config = json.loads(row['chunking_config'])
            embedding_config = json.loads(row['embedding_config'])
            llm_config = json.loads(row['llm_config'])
            
            return CollectionReadModel(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                chunking_config=ChunkingConfigReadModel(
                    size=chunking_config['size'],
                    overlap=chunking_config['overlap']
                ) if chunking_config else None,
                embedding_config=EmbeddingConfigReadModel(
                    model=embedding_config['model'],
                    base_url=embedding_config.get('base_url'),
                    api_key=embedding_config['api_key']
                ) if embedding_config else None,
                llm_config=LLMConfigReadModel(
                    model=llm_config['model'],
                    base_url=llm_config.get('base_url'),
                    api_key=llm_config['api_key']
                ) if llm_config else None,
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        except DatabaseError:
            raise
        except ValueError:
            raise
        except Exception as e:
            print(e)
            raise QueryFailed("GET_COLLECTION_BY_ID", e) from e
