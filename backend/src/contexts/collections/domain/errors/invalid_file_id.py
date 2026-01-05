from src.shared.domain.errors import DomainError


class InvalidFileId(DomainError):
    def __init__(self):
        super().__init__("File ID cannot be empty.")
