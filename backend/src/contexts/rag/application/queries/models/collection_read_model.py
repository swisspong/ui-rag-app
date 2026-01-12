from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class LLMConfigReadModel:
    model: str
    base_url: Optional[str]
    api_key: str


@dataclass
class EmbeddingConfigReadModel:
    model: str
    base_url: Optional[str]
    api_key: str


@dataclass
class ChunkingConfigReadModel:
    size: int
    overlap: int


@dataclass
class CollectionReadModel:
    id: str
    name: str
    description: str
    chunking_config: Optional[ChunkingConfigReadModel]
    llm_config: Optional[LLMConfigReadModel]
    embedding_config: Optional[EmbeddingConfigReadModel]
    created_at: datetime.datetime
    updated_at: datetime.datetime
