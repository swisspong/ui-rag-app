from src.shared.errors import BaseError


class ApplicationError(BaseError):
    status_code = 400
    error_code: str = "APPLICATION_ERROR"


class ConflictError(ApplicationError):
    status_code = 409
    error_code = "CONFLICT"


class InvalidInput(ApplicationError):
    status_code = 400
    error_code = "INVALID_INPUT"


class OperationFailed(ApplicationError):
    status_code = 500
    error_code = "OPERATION_FAILED"


class DependencyUnavailable(OperationFailed):
    error_code = "DEPENDENCY_UNAVAILABLE"
    status_code = 503


class NotFound(ApplicationError):
    status_code = 404
    error_code = "NOT_FOUND"

class UploadFailed(OperationFailed):
    error_code = "UPLOAD_FAILED"
