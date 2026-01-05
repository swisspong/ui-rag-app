from dataclasses import dataclass


@dataclass
class ProcessDocumentInternalInput:
    collection_id: str
    collection_file_id: str
    rag_process_id: str