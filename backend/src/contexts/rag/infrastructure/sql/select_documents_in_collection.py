SELECT_DOCUMENTS_IN_COLLECTION = """
SELECT
    d.id,
    d.name
FROM DOCUMENTS d
WHERE d.collection_id = $1
ORDER BY d.created_at DESC
"""
