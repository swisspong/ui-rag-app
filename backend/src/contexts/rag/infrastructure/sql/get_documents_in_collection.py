GET_DOCUMENTS_IN_COLLECTION = """
SELECT
    d.id,
    d.collection_file_id,
    a.filename,
    SUBSTRING(d.content, 1, 100) as content,
    d.created_at
FROM DOCUMENTS d
JOIN ASSETS a ON d.asset_id = a.id
WHERE d.collection_id = $1
ORDER BY d.created_at DESC
"""
