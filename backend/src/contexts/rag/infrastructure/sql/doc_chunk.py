

UPSERT_TEXT_CHUNK = """
INSERT INTO LIGHTRAG_DOC_CHUNKS (workspace, id, tokens,
chunk_order_index, full_doc_id, content, file_path, llm_cache_list,
create_time, update_time)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
ON CONFLICT (workspace,id) DO UPDATE
SET tokens=EXCLUDED.tokens,
chunk_order_index=EXCLUDED.chunk_order_index,
full_doc_id=EXCLUDED.full_doc_id,
content = EXCLUDED.content,
file_path=EXCLUDED.file_path,
llm_cache_list=EXCLUDED.llm_cache_list,
update_time = EXCLUDED.update_time
"""