SAVE_FILE = """
INSERT INTO FILES (id, collection_id, filename, content_type, size)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (id) DO UPDATE
SET collection_id=EXCLUDED.collection_id,
filename=EXCLUDED.filename,
content_type=EXCLUDED.content_type,
size=EXCLUDED.size
"""
