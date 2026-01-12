GET_ADDITIONAL_CHUNKS_IN_COLLECTION = """
    SELECT 
        id,
        content,
        meta,
        process_status,
        version,
        created_at
    FROM 
        chunks
    WHERE 
        collection_id = $1
        AND document_id IS NULL
        AND ($2::text IS NULL OR content ILIKE $2)
    ORDER BY 
        created_at DESC
    OFFSET $3
    LIMIT $4;
"""

COUNT_ADDITIONAL_CHUNKS_IN_COLLECTION = """
    SELECT 
        COUNT(*) as total
    FROM 
        chunks
    WHERE 
        collection_id = $1
        AND document_id IS NULL
        AND ($2::text IS NULL OR content ILIKE $2);
"""
