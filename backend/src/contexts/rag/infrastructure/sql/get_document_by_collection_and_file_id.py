GET_DOCUMENT_BY_COLLECTION_AND_FILE_ID = """
SELECT
    d.id,
    d.collection_id,
    d.collection_file_id,
    d.name,
    a.filename,
    d.status,
    d.content,
    d.created_at
FROM DOCUMENTS d
JOIN ASSETS a ON d.asset_id = a.id
WHERE d.collection_id = $1 AND d.collection_file_id = $2
LIMIT 1
"""
