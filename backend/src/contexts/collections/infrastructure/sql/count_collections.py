COUNT_COLLECTIONS = """
SELECT COUNT(*) as total_count
FROM collections
WHERE ($1::text IS NULL OR name ILIKE '%' || $1::text || '%' OR description ILIKE '%' || $1::text || '%')
"""