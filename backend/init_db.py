import asyncio
import asyncpg
from contextlib import asynccontextmanager
TABLES = {
    "COLLECTIONS": {
        "ddl": """CREATE TABLE COLLECTIONS (
                    id VARCHAR(255),
                    name VARCHAR(255),
                    description TEXT,
                    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    chunking_config JSONB DEFAULT '{}'::jsonb,
                    llm_config JSONB DEFAULT '{}'::jsonb,
                    embedding_config JSONB DEFAULT '{}'::jsonb,
	                CONSTRAINT COLLECTIONS_PK PRIMARY KEY (id)
                    )"""
    },
    "ASSETS": {
        "ddl": """CREATE TABLE ASSETS (
                    id VARCHAR(255),
                    filename VARCHAR(255),
                    content_type VARCHAR(255),
                    size INTEGER,
                    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
	                CONSTRAINT ASSETS_PK PRIMARY KEY (id)
                    )"""
    },
    "COLLECTION_FILES": {
        "ddl": """CREATE TABLE COLLECTION_FILES (
                    id VARCHAR(255),
                    collection_id VARCHAR(255),
                    asset_id VARCHAR(255),
                    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                 CONSTRAINT COLLECTION_FILES_PK PRIMARY KEY (id)
                    )"""
    },
    "DOCUMENTS": {
        "ddl": """CREATE TABLE DOCUMENTS (
                    id VARCHAR(255),
                    name VARCHAR(255),
                    collection_id VARCHAR(255),
                    collection_file_id VARCHAR(255),
                    content TEXT,
                    asset_id VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'PENDING',
                    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                 CONSTRAINT DOCUMENTS_PK PRIMARY KEY (id)
                    )"""
    },
    "CHUNKS": {
        "ddl": """CREATE TABLE CHUNKS (
                    id VARCHAR(255),
                    document_id VARCHAR(255) NULL,
                    collection_id VARCHAR(255),
                    content TEXT,
                    order_index INTEGER,
                    meta JSONB NULL DEFAULT '{}'::jsonb,
                    process_status VARCHAR(50) DEFAULT 'PENDING',
                    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
                    version INTEGER DEFAULT 1,
                 CONSTRAINT CHUNKS_PK PRIMARY KEY (id)
                    )"""
    }
}


class AsyncPGConnection:
    def __init__(self, dsn: str):
        self._dsn = dsn
        print("init db")
        print(dsn)
        self._pool = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(dsn=self._dsn, min_size=1, max_size=10)

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def transaction(self):
        """
        ใช้สำหรับ atomic operation เช่นใน use case หรือ repository ที่ต้องการ begin/commit
        """
        if not self._pool:
            raise RuntimeError(
                "Database pool not initialized. Call connect() first.")

        async with self._pool.acquire() as connection:
            async with connection.transaction():
                yield connection

    async def execute(self, query: str, *args):
        """
        Execute SQL (INSERT/UPDATE/DELETE)
        """
        async with self._pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        """
        Fetch หลายแถว (SELECT)
        """
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """
        Fetch แถวเดียว
        """
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *args)


async def main():
    dsn = "postgresql://postgres:postgres@localhost:5432/postgres"
    db = AsyncPGConnection(dsn)
    await db.connect()
    for k, v in TABLES.items():
        try:
            result = await db.fetchrow(f"SELECT 1 FROM {k} LIMIT 1")
            print(result)
        except Exception:
            print(f"Creating table {k}...")
            await db.execute(v["ddl"])

    # Migration: Add version column to CHUNKS if it doesn't exist
    try:
        check_version_col_sql = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='chunks' AND column_name='version'
        """
        has_version = await db.fetchrow(check_version_col_sql)
        if not has_version:
            print("Adding version column to CHUNKS table...")
            await db.execute("ALTER TABLE CHUNKS ADD COLUMN version INTEGER DEFAULT 1")
    except Exception as e:
        print(f"Failed to migrate CHUNKS table: {e}")

    # Migration: Add config columns to COLLECTIONS if they don't exist
    for col in ["chunking_config", "llm_config", "embedding_config"]:
        try:
            check_col_sql = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='collections' AND column_name='{col}'
            """
            has_col = await db.fetchrow(check_col_sql)
            if not has_col:
                print(f"Adding {col} column to COLLECTIONS table...")
                await db.execute(f"ALTER TABLE COLLECTIONS ADD COLUMN {col} JSONB DEFAULT '{{}}'::jsonb")
        except Exception as e:
            print(f"Failed to migrate COLLECTIONS table for column {col}: {e}")

    # Migration: Allow document_id to be NULL in CHUNKS
    try:
        print("Altering CHUNKS table to allow NULL document_id...")
        await db.execute("ALTER TABLE CHUNKS ALTER COLUMN document_id DROP NOT NULL")
    except Exception as e:
        print(f"Failed to alter CHUNKS table for document_id: {e}")

    table_names = list(TABLES.keys())
    table_names_lower = [t.lower() for t in table_names]
    check_all_indexes_sql = """
    SELECT indexname, tablename
    FROM pg_indexes
    WHERE tablename = ANY($1)
    """
    existing_indexes_result = await db.fetch(
        check_all_indexes_sql, [table_names_lower]
    )
    print(existing_indexes_result)
    if existing_indexes_result:
        for row in existing_indexes_result:
            print(
                f"Index {row['indexname']} on table {row['tablename']} already exists.")
    existing_indexes = set()
    if existing_indexes_result:
        existing_indexes = {row["indexname"]
                            for row in existing_indexes_result}
        # Create missing indexes
    for k in table_names:
        # Create index for id column if missing
        index_name = f"idx_{k.lower()}_id"
        if index_name not in existing_indexes:
            try:
                create_index_sql = f"CREATE INDEX {index_name} ON {k}(id)"

                await db.execute(create_index_sql)
            except Exception as e:
                print(
                    f"PostgreSQL, Failed to create index {index_name}, Got: {e}")

        # Create composite index for (workspace, id) if missing
        # composite_index_name = f"idx_{k.lower()}_workspace_id"
        # if composite_index_name not in existing_indexes:
        #     try:
        #         create_composite_index_sql = (
        #             f"CREATE INDEX {composite_index_name} ON {k}(workspace, id)"
        #         )
        #         print(
        #             f"PostgreSQL, Creating composite index {composite_index_name} on table {k}"
        #         )
        #         await db.execute(create_composite_index_sql)
        #     except Exception as e:
        #         print(
        #             f"PostgreSQL, Failed to create composite index {composite_index_name}, Got: {e}"
        #         )
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
