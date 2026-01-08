from dependency_injector import containers, providers


from src.contexts.rag.application.commands.process_document_internal.process_document_internal_handler import ProcessDocumentInternalHandler
from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_query import GetCollectionFileInCollectionQuery
from src.contexts.rag.infrastructure.services.celery_async_dispatcher import CeleryAsyncDispatcher
from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.shared.infrastructure.services.local_asset_storage import LocalAssetStorage
from src.shared.infrastructure.repositories.postgres_asset_repository import PostgresAssetRepository
from src.contexts.rag.infrastructure.repositories.postgres_collection_file_read_repository import PostgresCollectionFileReadRepository
from src.contexts.rag.infrastructure.services.thypoon_ocr import TyphoonOCR
from src.contexts.rag.infrastructure.repositories.postgres_document_repository import PostgresDocumentRepository
from src.contexts.rag.infrastructure.repositories.postgres_rag_process_repository import PostgresRAGProcessRepository
from src.shared.infrastructure.services.uuid_id_generator import UUIDIDGenerator


class WorkerContainer(containers.DeclarativeContainer):
    # config = providers.Configuration()

    database = providers.Singleton(
        AsyncPGConnection,
        # dsn=config.database_dsn
        dsn="postgresql://postgres:postgres@localhost:5432/postgres"
    )

    asset_storage = providers.Singleton(
        LocalAssetStorage,
        base_path="test"
    )

    asset_repository = providers.Singleton(
        PostgresAssetRepository,
        db=database
    )
    rag_process_repository = providers.Singleton(
        PostgresRAGProcessRepository,
        db=database
    )
    document_repository = providers.Singleton(
        PostgresDocumentRepository,
        db=database
    )
    collection_file_read_repository = providers.Singleton(
        PostgresCollectionFileReadRepository,
        db=database
    )
    id_generator = providers.Factory(
        UUIDIDGenerator
    )
    ocr = providers.Singleton(
        TyphoonOCR
    )
    get_collection_file_in_collection_query = providers.Factory(
        GetCollectionFileInCollectionQuery,
        collection_file_read_repository=collection_file_read_repository
    )

    process_document_internal_command = providers.Factory(
        ProcessDocumentInternalHandler,
        asset_storage=asset_storage,
        asset_repository=asset_repository,
        ocr=ocr,
        document_repository=document_repository,
        id_generator=id_generator,
        # rag_process_repository=rag_process_repository,
        get_collection_file_in_collection_query=get_collection_file_in_collection_query
    )
