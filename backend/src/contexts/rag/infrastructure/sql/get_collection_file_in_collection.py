GET_COLLECTION_FILE_IN_COLLECTION = """
SELECT id, collection_id, asset_id, created_at, updated_at FROM collection_files WHERE collection_id = $1 AND id = $2
"""
