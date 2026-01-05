GET_FILES_IN_COLLECTION = """
SELECT
    cf.id as collection_file_id,
    a.filename,
    a.size,
    cf.asset_id,
    cf.created_at,
    COALESCE(rp.current_stage, 'upload') as current_stage,
    COALESCE(rp.status, 'completed') as status
FROM collection_files cf
INNER JOIN assets a ON cf.asset_id = a.id
LEFT JOIN rag_process rp ON cf.id = rp.collection_file_id
WHERE cf.collection_id = $1
ORDER BY cf.created_at DESC
"""
