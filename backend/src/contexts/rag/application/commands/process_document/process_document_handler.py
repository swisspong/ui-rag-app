from src.shared.application.errors import NotFound
from src.shared.domain.repositories.asset_repository import AssetRepository
from src.shared.domain.value_objects.asset_id import AssetID
from src.contexts.rag.domain.repositories.document_repository import DocumentRepository
from src.contexts.rag.application.policies.document_name_policy import DocumentNamePolicy
from src.contexts.rag.domain.services.async_job_dispatcher import AsyncJobDispatcher
from src.contexts.rag.application.commands.process_document.process_document_input import ProcessDocumentInput
from src.shared.domain.services.id_generator import IDGenerator
from src.contexts.rag.domain.repositories.rag_process_repository import RAGProcessRepository
from src.contexts.rag.domain.entities.rag_process import RAGProcess
from src.contexts.rag.domain.value_objects.rag_process_id import RAGProcessID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_query import GetCollectionFileInCollectionQuery
from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_input import GetCollectionFileInCollectionInput
from src.contexts.rag.domain.entities.document import Document
from src.contexts.rag.domain.value_objects.document_name import DocumentName


class ProcessDocumentHandler:
    def __init__(
        self,
        job_dispatcher: AsyncJobDispatcher,
        id_generator: IDGenerator,
        get_collection_file_in_collection_query: GetCollectionFileInCollectionQuery,
        asset_repository: AssetRepository,
        document_repository: DocumentRepository,
        document_name_policy: DocumentNamePolicy
    ):
        self._job_dispatcher = job_dispatcher
        self._id_generator = id_generator
        self._get_collection_file_in_collection_query = get_collection_file_in_collection_query
        self._asset_repository = asset_repository
        self._document_repo = document_repository
        self._document_name_policy = document_name_policy

    async def execute(self, input: ProcessDocumentInput) -> None:
        for collection_file_id in input.collection_file_ids:
            collection_file = await self._get_collection_file_in_collection_query.execute(
                GetCollectionFileInCollectionInput(
                    collection_file_id=collection_file_id,
                    collection_id=input.collection_id
                )
            )
            if not collection_file:
                raise NotFound("Collection file not found")

            collection_id = CollectionID.from_value(input.collection_id)
            collection_file_id = CollectionFileID.from_value(
                collection_file_id)
            asset_id = AssetID.from_value(collection_file.asset_id)

            asset = await self._asset_repository.get_by_id(asset_id)

            if not asset:
                raise NotFound("Asset not found")

            resolved_name = await self._document_name_policy.resolve(collection_id, asset.filename)

            document = Document.create(
                id=DocumentID.from_value(self._id_generator.new_id()),
                name=DocumentName.from_value(resolved_name),
                collection_file_id=collection_file_id,
                collection_id=collection_id,
                content="",
                asset_id=asset_id
            )
            await self._document_repo.save(document)

            await self._job_dispatcher.dispatch(
                job_name="process_document_task",
                payload={
                    "document_id": document.id.value,
                }
            )
