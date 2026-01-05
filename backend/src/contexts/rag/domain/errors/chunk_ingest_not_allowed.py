from src.shared.domain.errors import DomainError


class ChunkIngestNotAllowed(DomainError):
    def __init__(self, process_status: str):
        super().__init__(
            f"Chunk ingest not allowed: process status is {process_status}"
        )
