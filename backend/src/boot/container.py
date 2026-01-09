from dependency_injector import containers, providers


from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.shared.infrastructure.services.uuid_id_generator import UUIDIDGenerator
from src.shared.infrastructure.services.local_asset_storage import LocalAssetStorage
from src.shared.infrastructure.repositories.postgres_asset_repository import PostgresAssetRepository
from src.contexts.collections.boot.container import CollectionContainer
from src.contexts.rag.boot.container import RAGContainer


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    database = providers.Singleton(
        AsyncPGConnection,
        dsn=config.database_dsn
    )
    asset_storage = providers.Singleton(
        LocalAssetStorage,
        base_path="test"
    )
    asset_repository = providers.Singleton(
        PostgresAssetRepository,
        db=database
    )

    id_generator = providers.Factory(
        UUIDIDGenerator
    )

    collection_package = providers.Container(
        CollectionContainer,
        database=database,
        id_generator=id_generator,
        asset_storage=asset_storage,
        asset_repository=asset_repository
    )

    rag_package = providers.Container(
        RAGContainer,
        database=database,
        id_generator=id_generator,
    )
