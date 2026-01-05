GET_ASSET_BY_ID = """
SELECT id, filename, content_type, size
FROM ASSETS
WHERE id = $1;
"""
