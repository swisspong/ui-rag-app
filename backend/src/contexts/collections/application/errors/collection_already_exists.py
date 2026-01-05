from src.shared.application.errors import ConflictError


class CollectionNameAlreadyExists(ConflictError):
    """
    Collection name must be unique.
    """

    error_code = "COLLECTION_NAME_ALREADY_EXISTS"

    def __init__(self, name: str):
        super().__init__(f"Collection with name '{name}' already exists.")
        self.name = name
