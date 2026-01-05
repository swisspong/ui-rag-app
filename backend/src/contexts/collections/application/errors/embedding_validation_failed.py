from src.shared.application.errors import ApplicationError


class EmbeddingValidationFailed(ApplicationError):
    """
    Embedding configuration is invalid or cannot be verified
    against external provider.
    """

    error_code = "EMBEDDING_VALIDATION_FAILED"

    def __init__(self, reason: str):
        super().__init__(f"Embedding validation failed: {reason}")
        self.reason = reason
