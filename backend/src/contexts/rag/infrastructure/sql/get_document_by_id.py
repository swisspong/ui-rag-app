GET_DOCUMENT_BY_ID = """
SELECT id, collection_id, collection_file_id, content, asset_id FROM documents WHERE id = $1
"""