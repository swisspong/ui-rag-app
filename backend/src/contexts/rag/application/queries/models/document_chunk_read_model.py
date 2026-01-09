from dataclasses import dataclass

@dataclass
class DocumentChunkReadModel:
    id: str
    content: str
    meta: dict
    status: str
