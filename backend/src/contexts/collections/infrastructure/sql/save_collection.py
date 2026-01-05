SAVE_COLLECTION = """
INSERT INTO COLLECTIONS (id, name, description, created_at, updated_at)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (id) DO UPDATE
SET name=EXCLUDED.name,
description=EXCLUDED.description,
created_at=EXCLUDED.created_at,
updated_at=EXCLUDED.updated_at
"""
