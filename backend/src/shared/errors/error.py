class Error(Exception):
    """Root class for all custom errors across the system."""
    code: str = "error"
    status_code: int = 500  # Default HTTP status (can override)
    
    def __init__(self, message: str, *, code: str | None = None, status_code: int | None = None):
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        super().__init__(message)

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message}

