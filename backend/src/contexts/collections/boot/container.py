from dependency_injector import containers, providers
from src.contexts.collections.infrastructure.repositories.postgres_collection_read_repository import PostgresCollectionReadRepository
from src.contexts.collections.infrastructure.repositories.postgres_collection_repository import PostgresCollectionRepository
from src.contexts.collections.infrastructure.repositories.postgres_collection_file_repository import PostgresCollectionFileRepository
from src.contexts.collections.application.queries.collection_name_exists.collection_name_exsits_query import CollectionNameExistsQuery
from src.contexts.collections.application.queries.get_collection_list.get_collection_list_query import GetCollectionListQuery
from src.contexts.collections.application.queries.get_files_in_collection.get_files_in_collection_query import GetFilesInCollectionQuery
from src.contexts.collections.application.commands.create_collection.create_collection_handler import CreateCollectionHandler
from src.contexts.collections.application.commands.upload_files_for_collection.upload_files_handler import UploadFilesHandler
from src.contexts.collections.application.policies.embedding_validation import EmbeddingValidation
from src.contexts.collections.application.policies.llm_validatoin import LLMValidation
from src.contexts.collections.application.policies.collection_filename_policy import CollectionFilenamePolicy
from src.contexts.collections.infrastructure.repositories.postgres_file_repository import PostgresFileRepository
from src.contexts.collections.infrastructure.services.local_file_storage import LocalFileStorage


class CollectionContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    id_generator = providers.Dependency()
    asset_storage = providers.Dependency()
    asset_repository = providers.Dependency()

    collection_read_repository = providers.Singleton(
        PostgresCollectionReadRepository,
        db=database,
    )

    collection_repository = providers.Singleton(
        PostgresCollectionRepository,
        db=database,
    )

    collection_file_repository = providers.Singleton(
        PostgresCollectionFileRepository,
        db=database,
    )

    collection_filename_policy = providers.Singleton(
        CollectionFilenamePolicy,
        collection_file_repository=collection_file_repository,
        asset_repository=asset_repository
    )

    # file_repository = providers.Singleton(
    #     PostgresFileRepository,
    #     db=database,
    # )

    # file_storage = providers.Singleton(
    #     LocalFileStorage,
    #     base_path="test"
    # )

    llm_validation = providers.Singleton(
        LLMValidation,
    )

    embedding_validation = providers.Singleton(
        EmbeddingValidation,
    )

    collection_name_exists_query = providers.Factory(
        CollectionNameExistsQuery,
        collection_read_repository=collection_read_repository,
    )

    get_collection_list_query = providers.Factory(
        GetCollectionListQuery,
        collection_read_repository=collection_read_repository,
    )

    get_files_in_collection_query = providers.Factory(
        GetFilesInCollectionQuery,
        collection_read_repository=collection_read_repository,
    )

    create_collection_command = providers.Factory(
        CreateCollectionHandler,
        collection_name_exists=collection_name_exists_query,
        llm_validation=llm_validation,
        embedding_validation=embedding_validation,
        collection_repository=collection_repository,
        id_generator=id_generator
    )
    upload_files_command = providers.Factory(
        UploadFilesHandler,
        asset_storage=asset_storage,
        id_generator=id_generator,
        asset_repository=asset_repository,
        filename_policy=collection_filename_policy,
        collection_file_repository=collection_file_repository
    )
