from dataclasses import dataclass


@dataclass
class IngestInput:
    workspace: str
    content: str
    max_token_size: int = 1024
    overlap_token_size: int = 128
    max_batch_size = 10
    doc_id = "doc-123"
    file_path = "test"
