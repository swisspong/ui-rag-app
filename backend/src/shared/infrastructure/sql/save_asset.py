SAVE_ASSET = """
INSERT INTO ASSETS (id, filename, content_type, size)
VALUES ($1, $2, $3, $4)
ON CONFLICT (id) DO UPDATE
SET filename=EXCLUDED.filename,
content_type=EXCLUDED.content_type,
size=EXCLUDED.size
"""
