GET_DOCUMENT_BY_ID = """
SELECT id, name, collection_id, collection_file_id, content, asset_id, status FROM documents WHERE id = $1
"""
