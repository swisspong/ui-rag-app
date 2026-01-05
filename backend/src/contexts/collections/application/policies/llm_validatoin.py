from src.contexts.collections.domain.value_objects.llm_config import LLMConfig


class LLMValidation:
    async def validate(self, config: LLMConfig) -> bool:
        return True
