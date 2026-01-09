GET_CHUNKS_WITH_PAGINATION = """
SELECT
    id,
    content,
    meta,
    process_status as status
FROM chunks
WHERE collection_id = $1
AND document_id = $2
AND version = $3
AND (
    $4::text IS NULL OR content ILIKE $4
)
ORDER BY order_index ASC
OFFSET $5 LIMIT $6
"""

COUNT_CHUNKS = """
SELECT COUNT(*) as total
FROM chunks
WHERE collection_id = $1
AND document_id = $2
AND version = $3
AND (
    $4::text IS NULL OR content ILIKE $4
)
"""
