GET_CHUNKS_BY_COLLECTION_AND_FILE_ID = """
SELECT
    c.id,
    c.collection_id,
    c.document_id,
    c.content,
    c.meta,
    c.order_index,
    c.process_status,
    c.created_at,
    c.updated_at
FROM chunks c
INNER JOIN documents d ON c.document_id = d.id
WHERE c.collection_id = $1
AND d.collection_file_id = $2
ORDER BY c.created_at DESC, c.order_index ASC
"""
