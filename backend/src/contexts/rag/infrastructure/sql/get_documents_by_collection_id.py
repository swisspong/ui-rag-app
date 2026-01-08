GET_DOCUMENTS_BY_COLLECTION_ID = """
SELECT id, name, collection_id, collection_file_id, content, asset_id, status
FROM documents
WHERE collection_id = $1
"""
