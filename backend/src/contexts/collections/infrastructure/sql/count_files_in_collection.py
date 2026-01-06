COUNT_FILES_IN_COLLECTION = """
SELECT COUNT(*) as total_count
FROM collection_files cf
INNER JOIN assets a ON cf.asset_id = a.id
WHERE cf.collection_id = $1
AND ($2::text IS NULL OR a.filename ILIKE '%' || $2::text || '%')
"""
