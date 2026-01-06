GET_FILES_IN_COLLECTION = """
SELECT
    cf.id,
    a.filename,
    a.size,
    a.content_type,
    cf.created_at
FROM collection_files cf
INNER JOIN assets a ON cf.asset_id = a.id
WHERE cf.collection_id = $1
AND ($2::text IS NULL OR a.filename ILIKE '%' || $2::text || '%')
ORDER BY CASE
    WHEN $3 = 'created_at' THEN cf.created_at::text
    WHEN $3 = 'filename' THEN a.filename
    ELSE cf.created_at::text
END DESC
LIMIT $4 OFFSET $5
"""
