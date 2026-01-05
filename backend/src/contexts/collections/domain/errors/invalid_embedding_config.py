from .....shared.domain.errors import DomainError


class InvalidEmbeddingConfig(DomainError):
    def __init__(self, reason: str):
        super().__init__(f"Invalid embedding config: {reason}")
