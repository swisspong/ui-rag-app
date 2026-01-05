SAVE_DOCUMENT = """
INSERT INTO DOCUMENTS (id, collection_id, collection_file_id, content, asset_id)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (id) DO UPDATE
SET collection_id=EXCLUDED.collection_id,
collection_file_id=EXCLUDED.collection_file_id,
content=EXCLUDED.content,
asset_id=EXCLUDED.asset_id
"""
