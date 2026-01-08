GET_DOCUMENTS_IN_COLLECTION = """
SELECT
    d.id,
    d.collection_file_id,
    d.name,
    a.filename,
    d.status,
    SUBSTRING(d.content, 1, 100) as content,
    d.created_at
FROM DOCUMENTS d
JOIN ASSETS a ON d.asset_id = a.id
WHERE d.collection_id = $1
  AND ($2::text IS NULL OR a.filename ILIKE '%' || $2::text || '%' OR d.content ILIKE '%' || $2::text || '%')
ORDER BY d.created_at DESC
LIMIT $3
OFFSET $4
"""
