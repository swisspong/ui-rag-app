GET_ALL_CHUNKS_BY_COLLECTION_ID = """
SELECT
    id,
    collection_id,
    document_id,
    content,
    meta,
    order_index,
    process_status,
    created_at,
    updated_at
FROM chunks
WHERE collection_id = $1
ORDER BY created_at DESC, order_index ASC
"""
