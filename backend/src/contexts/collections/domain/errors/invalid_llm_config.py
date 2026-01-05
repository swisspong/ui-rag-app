from .....shared.domain.errors import DomainError


class InvalidLLMConfig(DomainError):
    def __init__(self, reason: str):
        super().__init__(f"Invalid llm config: {reason}")
