from pydantic_settings import BaseSettings
from pydantic import Field

from src.contexts.rag.infrastructure.configs.embedding_settings import EmbeddingSettings


class Settings(BaseSettings):
    database_dsn: str = Field(..., env="DATABASE_DSN")
    enable_config_mode: bool = Field(default=False, env="ENABLE_CONFIG_MODE")

    embedding: EmbeddingSettings = Field(..., env="EMBEDDING")
    class Config:
        env_file = ".env"
