GET_COLLECTION_FILE_MANY_BY_COLLECTION_ID = """
SELECT
    id,
    collection_id,
    asset_id,
    created_at,
    updated_at
FROM collection_files
WHERE collection_id = $1
"""
