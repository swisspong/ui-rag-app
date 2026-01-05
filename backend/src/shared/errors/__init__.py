class BaseError(Exception):
    error_code: str = "UNKNOWN_ERROR"
    status_code: int = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message