GET_CHUNK_BY_ID_AND_COLLECTION_ID = """
SELECT
    id,
    document_id,
    collection_id,
    content,
    order_index,
    meta,
    process_status,
    created_at,
    updated_at
FROM chunks
WHERE id = $1
AND collection_id = $2
"""
