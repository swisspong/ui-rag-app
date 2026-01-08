SAVE_DOCUMENT = """
INSERT INTO DOCUMENTS (id, name, collection_id, collection_file_id, content, asset_id, status)
VALUES ($1, $2, $3, $4, $5, $6, $7)
ON CONFLICT (id) DO UPDATE
SET collection_id=EXCLUDED.collection_id,
collection_file_id=EXCLUDED.collection_file_id,
content=EXCLUDED.content,
asset_id=EXCLUDED.asset_id,
status=EXCLUDED.status
"""
