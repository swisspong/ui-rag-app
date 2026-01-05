GET_CHUNKS_BY_COLLECTION_ID = """
SELECT
    id,
    document_id,
    collection_id,
    content,
    order_index,
    meta,
    created_at,
    updated_at
FROM chunks
WHERE collection_id = $1
AND document_id = $2
"""
