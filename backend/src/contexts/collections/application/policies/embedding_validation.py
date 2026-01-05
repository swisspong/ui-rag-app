from src.contexts.collections.domain.value_objects.embedding_config import EmbeddingConfig


class EmbeddingValidation:
    async def validate(self, config: EmbeddingConfig) -> bool:
        return True
