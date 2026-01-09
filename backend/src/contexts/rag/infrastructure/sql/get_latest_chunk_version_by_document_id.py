GET_LATEST_CHUNK_VERSION_BY_DOCUMENT_ID = """
SELECT MAX(version) as latest_version
FROM chunks
WHERE collection_id = $1 AND document_id = $2
"""
