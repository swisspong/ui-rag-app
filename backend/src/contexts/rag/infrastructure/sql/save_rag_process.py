SAVE_RAG_PROCESS = """
INSERT INTO RAG_PROCESS (id, collection_id, collection_file_id, status, current_stage, ocr_status, ocr_started_at, ocr_finished_at, ingest_status, ingest_started_at, ingest_finished_at, chunking_status, chunking_started_at, chunking_finished_at, error_code, error_message, document_id)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
ON CONFLICT (id) DO UPDATE
SET collection_id=EXCLUDED.collection_id,
collection_file_id=EXCLUDED.collection_file_id,
status=EXCLUDED.status,
current_stage=EXCLUDED.current_stage,
ocr_status=EXCLUDED.ocr_status,
ocr_started_at=EXCLUDED.ocr_started_at,
ocr_finished_at=EXCLUDED.ocr_finished_at,
ingest_status=EXCLUDED.ingest_status,
ingest_started_at=EXCLUDED.ingest_started_at,
ingest_finished_at=EXCLUDED.ingest_finished_at,
chunking_status=EXCLUDED.chunking_status,
chunking_started_at=EXCLUDED.chunking_started_at,
chunking_finished_at=EXCLUDED.chunking_finished_at,
error_code=EXCLUDED.error_code,
error_message=EXCLUDED.error_message,
document_id=EXCLUDED.document_id
"""
