from dependency_injector import containers, providers

from src.contexts.rag.application.commands.process_document.process_document_handler import ProcessDocumentHandler
from src.contexts.rag.infrastructure.services.celery_async_dispatcher import CeleryAsyncDispatcher
from src.contexts.rag.infrastructure.queues.celery_app import celery_app
from src.contexts.rag.infrastructure.repositories.postgres_chunk_repository import PostgresChunkRepository
from src.contexts.rag.application.commands.chunking.chunking_handler import ChunkingHandler
from src.contexts.rag.infrastructure.services.tiktoken_tokenizer import TiktokenTokenizer
from src.contexts.rag.infrastructure.services.openai_embedding import OpenAIEmbedding
from src.contexts.rag.infrastructure.repositories.postgres_document_repository import PostgresDocumentRepository
from src.contexts.rag.infrastructure.repositories.postgres_rag_process_repository import PostgresRAGProcessRepository
from src.contexts.rag.infrastructure.repositories.postgres_collection_read_repository import PostgresCollectionReadRepository
from src.contexts.rag.application.queries.get_collection.get_collection_query import GetCollectionQuery
from src.contexts.rag.application.commands.ingest_by_document_in_collection.ingest_by_document_in_collection_handler import IngestByDocumentInCollectionHandler
from src.contexts.rag.infrastructure.database.milvus_connection import MilvusConnection
from src.contexts.rag.infrastructure.repositories.milvus_vector_repository import MilvusVectorRepository
from src.contexts.rag.infrastructure.repositories.postgres_document_read_repository import PostgresDocumentReadRepository
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_query import GetDocumentsInCollectionQuery
from src.contexts.rag.infrastructure.repositories.postgres_chunk_read_repository import PostgresChunkReadRepository
from src.contexts.rag.application.queries.get_chunks_by_collection_file_id.get_chunks_by_collection_file_id_query import GetChunksByCollectionFileIdQuery
from src.contexts.rag.application.queries.get_document_by_collection_and_file_id.get_document_by_collection_and_file_id_query import GetDocumentByCollectionAndFileIdQuery
from src.contexts.rag.application.queries.get_chunk_by_id_and_collection_id.get_chunk_by_id_and_collection_id_query import GetChunkByIdAndCollectionIdQuery
from src.contexts.rag.application.queries.get_chunks_by_collection_id.get_chunks_by_collection_id_query import GetChunksByCollectionIdQuery
from src.contexts.rag.application.commands.update_chunk.update_chunk_handler import UpdateChunkHandler
from src.contexts.rag.application.commands.delete_multiple_chunks.delete_multiple_chunks_handler import DeleteMultipleChunksHandler
from src.contexts.rag.application.commands.ingest_multiple_chunks_by_collection.ingest_multiple_chunks_by_collection_handler import IngestMultipleChunksByCollectionHandler

class RAGContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    id_generator = providers.Dependency()

    celery_app = providers.Object(celery_app)

    async_dispatcher = providers.Singleton(
        CeleryAsyncDispatcher,
        celery_app=celery_app
    )
    rag_process_repository = providers.Singleton(
        PostgresRAGProcessRepository,
        db=database
    )
    chunk_repository = providers.Singleton(
        PostgresChunkRepository,
        db=database
    )
    document_repository = providers.Singleton(
        PostgresDocumentRepository,
        db=database
    )
    collection_read_repository = providers.Singleton(
        PostgresCollectionReadRepository,
        db=database
    )
    document_read_repository = providers.Singleton(
        PostgresDocumentReadRepository,
        db=database
    )
    chunk_read_repository = providers.Singleton(
        PostgresChunkReadRepository,
        db=database
    )

    milvus_connection = providers.Singleton(
        MilvusConnection,
        host="localhost",
        port=19530,
        user="",
        password="",
        db_name="default"
    )

    vector_repository = providers.Singleton(
        MilvusVectorRepository,
        connection=milvus_connection
    )

    tokenizer = providers.Factory(
        TiktokenTokenizer
    )

    embedding = providers.Factory(
        OpenAIEmbedding,
        api_key=None,
        base_url=None,
        model=None
    )

    process_document_handler = providers.Factory(
        ProcessDocumentHandler,
        job_dispatcher=async_dispatcher,
        id_generator=id_generator,
        rag_process_repository=rag_process_repository
    )
    
    chunking_handler = providers.Factory(
        ChunkingHandler,
        tokenizer=tokenizer,
        chunk_repository=chunk_repository,
        document_repository=document_repository,
        id_generator=id_generator,
        rag_process_repository=rag_process_repository
    )
    
    get_collection_query = providers.Factory(
        GetCollectionQuery,
        collection_read_repository=collection_read_repository
    )
    get_documents_in_collection_query = providers.Factory(
        GetDocumentsInCollectionQuery,
        document_read_repository=document_read_repository
    )
    get_chunks_by_collection_file_id_query = providers.Factory(
        GetChunksByCollectionFileIdQuery,
        chunk_read_repository=chunk_read_repository
    )
    get_document_by_collection_and_file_id_query = providers.Factory(
        GetDocumentByCollectionAndFileIdQuery,
        document_read_repository=document_read_repository
    )
    get_chunk_by_id_and_collection_id_query = providers.Factory(
        GetChunkByIdAndCollectionIdQuery,
        chunk_read_repository=chunk_read_repository
    )
    get_chunks_by_collection_id_query = providers.Factory(
        GetChunksByCollectionIdQuery,
        chunk_read_repository=chunk_read_repository
    )

    ingest_by_document_in_collection_handler = providers.Factory(
        IngestByDocumentInCollectionHandler,
        embedding=embedding,
        id_generator=id_generator,
        vector_repo=vector_repository,
        get_collection_query=get_collection_query,
        chunk_repository=chunk_repository,
        rag_process_repository=rag_process_repository
    )

    update_chunk_handler = providers.Factory(
        UpdateChunkHandler,
        chunk_repository=chunk_repository
    )

    delete_multiple_chunks_handler = providers.Factory(
        DeleteMultipleChunksHandler,
        chunk_repository=chunk_repository
    )

    ingest_multiple_chunks_by_collection_handler = providers.Factory(
        IngestMultipleChunksByCollectionHandler,
        chunk_repository=chunk_repository,
        vector_repository=vector_repository,
        embedding_service=embedding,
        id_generator=id_generator,
        get_collection_query=get_collection_query
    )
