from fastapi import APIRouter

router = APIRouter(prefix="/collections", tags=["RAG"])

from . import (
    process_ocr,
    chunking,
    ingest,
    get_documents_in_collection,
    get_chunks_by_collection_file_id,
    get_document_by_collection_and_file_id,
    get_chunk_by_id_and_collection_id,
    get_chunks_by_collection_id,
    update_chunk,
    delete_multiple_chunks,
    ingest_multiple_chunks_by_collection,
    ingest_multiple_chunks_by_collection,
    get_document_chunks_in_collection,
    get_chunks_by_document_id,
    get_additional_chunks_in_collection
)
