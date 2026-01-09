GET_DOCUMENT_SUMMARIES_IN_COLLECTION = """
SELECT
    c.document_id as id,
    c.version,
    d.name,
    COUNT(c.id) as chunk_count,
    MAX(c.created_at) as created_at
FROM chunks c
JOIN documents d ON c.document_id = d.id
WHERE c.collection_id = $1
AND ($2::text IS NULL OR d.name ILIKE $2)
GROUP BY c.document_id, c.version, d.name
ORDER BY created_at DESC
OFFSET $3 LIMIT $4
"""

COUNT_DOCUMENT_SUMMARIES_IN_COLLECTION = """
SELECT COUNT(*) as total FROM (
    SELECT c.document_id, c.version
    FROM chunks c
    JOIN documents d ON c.document_id = d.id
    WHERE c.collection_id = $1
    AND ($2::text IS NULL OR d.name ILIKE $2)
    GROUP BY c.document_id, c.version, d.name
) as sub
"""
