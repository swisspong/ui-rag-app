from .....shared.domain.errors import DomainError


class InvalidCollectionId(DomainError):
    def __init__(self):
        super().__init__("Collection ID cannot be empty.")
