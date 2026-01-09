SAVE_CHUNK = """
INSERT INTO CHUNKS (id, document_id, collection_id, content, order_index, meta, process_status, created_at, updated_at, version)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
ON CONFLICT (id) DO UPDATE
SET document_id=EXCLUDED.document_id,
collection_id=EXCLUDED.collection_id,
content=EXCLUDED.content,
order_index=EXCLUDED.order_index,
meta=EXCLUDED.meta,
process_status=EXCLUDED.process_status,
created_at=EXCLUDED.created_at,
updated_at=EXCLUDED.updated_at,
version=EXCLUDED.version
"""
