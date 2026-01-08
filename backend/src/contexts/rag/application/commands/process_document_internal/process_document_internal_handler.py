import asyncio
from src.shared.domain.services.asset_storage import AssetStorage
from src.shared.domain.repositories.asset_repository import AssetRepository
from src.contexts.rag.domain.services.ocr import OCR
from src.shared.domain.value_objects.asset_id import AssetID
from src.shared.application.errors import NotFound

from src.contexts.rag.domain.repositories.document_repository import DocumentRepository
from src.contexts.rag.domain.entities.document import Document
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID
from src.contexts.rag.domain.value_objects.document_id import DocumentID
from src.shared.domain.services.id_generator import IDGenerator
from src.contexts.rag.application.commands.process_document_internal.process_document_internal_input import ProcessDocumentInternalInput
from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_input import GetCollectionFileInCollectionInput
from src.contexts.rag.application.queries.get_collection_file_in_collection.get_collection_file_in_collection_query import GetCollectionFileInCollectionQuery


class ProcessDocumentInternalHandler:
    def __init__(
        self,
        asset_storage: AssetStorage,
        asset_repository: AssetRepository,
        ocr: OCR,
        document_repository: DocumentRepository,
        id_generator: IDGenerator,
        get_collection_file_in_collection_query: GetCollectionFileInCollectionQuery
    ):
        self._asset_storage = asset_storage
        self._asset_repository = asset_repository
        self._ocr = ocr
        self._document_repo = document_repository
        self._id_generator = id_generator
        self._get_collection_file_in_collection_query = get_collection_file_in_collection_query

    async def execute(self, input: ProcessDocumentInternalInput):

        document_id = DocumentID.from_value(input.document_id)

        document = await self._document_repo.get_by_id(document_id)
        if not document:
            raise NotFound("Document not found")

        document.mark_as_running()
        await self._document_repo.save(document)

        asset = await self._asset_repository.get_by_id(document.asset_id)

        if not asset:
            raise NotFound("Asset not found")

        a = await self._asset_storage.open(document.asset_id)

        result = await self._ocr.extract_text(asset, a)

        document.mark_as_completed(result)

        await self._document_repo.save(document)
