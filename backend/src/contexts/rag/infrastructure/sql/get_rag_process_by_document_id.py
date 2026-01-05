GET_RAG_PROCESS_BY_DOCUMENT_ID = """
SELECT id, collection_id, collection_file_id, status, current_stage,
       ocr_status, ocr_started_at, ocr_finished_at,
       ingest_status, ingest_started_at, ingest_finished_at,
       chunking_status, chunking_started_at, chunking_finished_at,
       error_code, error_message, document_id, created_at, updated_at
FROM RAG_PROCESS
WHERE document_id = $1 AND collection_id = $2;
"""
