SAVE_COLLECTION_FILE = """
INSERT INTO COLLECTION_FILES (id, collection_id, asset_id, created_at, updated_at)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (id) DO UPDATE
SET collection_id=EXCLUDED.collection_id,
asset_id=EXCLUDED.asset_id,
created_at=EXCLUDED.created_at,
updated_at=EXCLUDED.updated_at
"""
