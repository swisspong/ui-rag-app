from src.shared.domain.services.id_generator import IDGenerator
from src.contexts.collections.domain.entities.collection import Collection
from src.contexts.collections.domain.value_objects.collection_name import CollectionName
from src.contexts.collections.domain.value_objects.collection_description import CollectionDescription
from src.contexts.collections.domain.repositories.collection_repository import CollectionRepository
from src.contexts.collections.application.errors.collection_already_exists import CollectionNameAlreadyExists
from src.contexts.collections.application.policies.llm_validatoin import LLMValidation
from src.contexts.collections.application.policies.embedding_validation import EmbeddingValidation
from src.contexts.collections.application.commands.create_collection.create_collection_input import CreateCollectionInput
from src.contexts.collections.application.commands.create_collection.create_collection_output import (
    CreateCollectionOutput,
)
from src.contexts.collections.application.queries.collection_name_exists.collection_name_exsits_query import CollectionNameExistsQuery
from src.shared.domain.errors import DomainError
from src.shared.infrastructure.errors import (
    InfrastructureError,
    DuplicateRecordError,
)
from src.shared.application.errors import (
    InvalidInput,

    DependencyUnavailable
)


class CreateCollectionHandler:
    def __init__(
        self,
        collection_name_exists: CollectionNameExistsQuery,
        llm_validation: LLMValidation,
        embedding_validation: EmbeddingValidation,
        collection_repository: CollectionRepository,
        id_generator: IDGenerator
    ):
        self._collection_name_exists = collection_name_exists
        self._llm_validation = llm_validation
        self._embedding_validation = embedding_validation
        self._collection_repo = collection_repository
        self._id_generator = id_generator

    async def execute(
        self,
        input: CreateCollectionInput
    ):
        try:

            name = CollectionName.from_value(input.name)
            description = CollectionDescription.from_value(input.name)
        except DomainError as e:
            raise InvalidInput(str(e)) from e

        try:
            name_exists = await self._collection_name_exists.execute(
                name
            )
        except InfrastructureError as e:
            raise DependencyUnavailable(
                "Failed to check collection name uniqueness"
            ) from e

        if name_exists:
            raise CollectionNameAlreadyExists(
                name.value
            )


        collection = Collection.create(
            id=self._id_generator,
            name=name,
            description=description,
        )

        try:
            collection = await self._collection_repo.save(collection)
        except DuplicateRecordError as e:
            raise CollectionNameAlreadyExists(name.value) from e
        except InfrastructureError as e:
            raise DependencyUnavailable("Failed to create collection") from e

        return CreateCollectionOutput(
            id=collection.id.value,
            name=collection.name.value,
            description=collection.description.value,
            created_at=collection.created_at
        )
