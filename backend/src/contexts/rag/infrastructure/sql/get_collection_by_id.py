GET_COLLECTION_BY_ID = """
SELECT
    id,
    name,
    description,
    chunking_config,
    embedding_config,
    llm_config,
    created_at,
    updated_at
FROM collections
WHERE id = $1
"""
