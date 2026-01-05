GET_COLLECTION_LIST = """
SELECT
    c.id,
    c.name,
    c.description,
    COUNT(cf.id) AS file_count,
    c.created_at,
    c.updated_at
FROM collections c
LEFT JOIN collection_files cf ON c.id = cf.collection_id
WHERE ($1::text IS NULL OR c.name ILIKE '%' || $1::text || '%' OR c.description ILIKE '%' || $1::text || '%')
GROUP BY c.id, c.name, c.description, c.created_at, c.updated_at
ORDER BY CASE
    WHEN $2 = 'name' THEN c.name
    WHEN $2 = 'created_at' THEN c.created_at::text
    WHEN $2 = 'updated_at' THEN c.updated_at::text
    ELSE c.created_at::text
END
LIMIT $3
OFFSET $4
"""