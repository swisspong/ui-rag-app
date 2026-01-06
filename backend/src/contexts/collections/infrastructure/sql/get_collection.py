GET_COLLECTION = """
SELECT
    c.id,
    c.name,
    c.description,
    COUNT(cf.id) AS file_count,
    c.created_at,
    c.updated_at
FROM collections c
LEFT JOIN collection_files cf ON c.id = cf.collection_id
WHERE c.id = $1::text
GROUP BY c.id, c.name, c.description, c.created_at, c.updated_at
"""
