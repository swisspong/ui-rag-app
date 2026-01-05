from src.shared.application.errors import ApplicationError


class LLMValidationFailed(ApplicationError):
    """
    LLM configuration is invalid or cannot be verified
    against external provider.
    """

    error_code = "LLM_VALIDATION_FAILED"

    def __init__(self, reason: str):
        super().__init__(f"LLM validation failed: {reason}")
        self.reason = reason
