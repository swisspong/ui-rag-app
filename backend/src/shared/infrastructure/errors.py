from src.shared.errors import BaseError


class InfrastructureError(BaseError):
    pass


class DatabaseError(InfrastructureError):
    pass


class InfrastructureUnavailableError(InfrastructureError):
    pass


class DuplicateRecordError(InfrastructureError):
    pass


class QueryFailed(InfrastructureError):
    def __init__(self, query_name: str, original: Exception):
        super().__init__(f"Query failed: {query_name}")
        self.query_name = query_name
        self.original = original

class FileStorageError(InfrastructureError):
    pass


class FileNotFoundStorageError(FileStorageError):
    pass


class FileWriteFailed(FileStorageError):
    pass


class FileDeleteFailed(FileStorageError):
    pass