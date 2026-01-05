from src.shared.domain.errors import DomainError


class InvalidChunkingConfig(DomainError):
    def __init__(self, size: int, overlap: int, reason: str):
        super().__init__(
            f"Invalid chunking config (size={size}, overlap={overlap}): {reason}"
        )
