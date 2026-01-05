DELETE_CHUNK_BY_ID_AND_COLLECTION_ID = """
DELETE FROM chunks
WHERE id = $1
AND collection_id = $2
"""
