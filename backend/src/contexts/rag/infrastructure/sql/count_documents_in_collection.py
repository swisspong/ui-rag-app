COUNT_DOCUMENTS_IN_COLLECTION = """
SELECT COUNT(d.id)
FROM DOCUMENTS d
JOIN ASSETS a ON d.asset_id = a.id
WHERE d.collection_id = $1
  AND ($2::text IS NULL OR a.filename ILIKE '%' || $2::text || '%' OR d.content ILIKE '%' || $2::text || '%')
"""
