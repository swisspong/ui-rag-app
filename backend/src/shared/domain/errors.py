from src.shared.errors import BaseError


class DomainError(BaseError):
    pass


class ConflictError(DomainError):
    pass


class PersistenceError(DomainError):
    pass
