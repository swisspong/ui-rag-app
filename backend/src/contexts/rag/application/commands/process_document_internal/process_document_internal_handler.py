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
from src.contexts.rag.domain.entities.rag_process import RAGProcess
from src.contexts.rag.domain.repositories.rag_process_repository import RAGProcessRepository
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
        rag_process_repository: RAGProcessRepository,
        get_collection_file_in_collection_query: GetCollectionFileInCollectionQuery
    ):
        self._asset_storage = asset_storage
        self._asset_repository = asset_repository
        self._ocr = ocr
        self._document_repo = document_repository
        self._id_generator = id_generator
        self._rag_process_repository = rag_process_repository
        self._get_collection_file_in_collection_query = get_collection_file_in_collection_query

    async def execute(self, input: ProcessDocumentInternalInput):
        await asyncio.sleep(4)
        print(input.collection_file_id)
        collection_file = await self._get_collection_file_in_collection_query.execute(
            GetCollectionFileInCollectionInput(
                collection_file_id=input.collection_file_id,
                collection_id=input.collection_id
            )
        )
        if not collection_file:
            raise NotFound("Collection file not found")

        # Load existing RAGProcess from repository
        collection_id = CollectionID.from_value(input.collection_id)
        collection_file_id = CollectionFileID.from_value(
            input.collection_file_id)
        rag_process = await self._rag_process_repository.get_by_collection_id_and_collection_file_id(
            collection_id,
            collection_file_id
        )

        if not rag_process:
            raise NotFound("RAG process not found")

        asset_id = AssetID.from_value(collection_file.asset_id)

        asset = await self._asset_repository.get_by_id(asset_id)

        if not asset:
            raise NotFound("Asset not found")

        a = await self._asset_storage.open(asset_id)

        rag_process.start_ocr()
        await self._rag_process_repository.save(rag_process)

        result = await self._ocr.extract_text(asset, a)

        document = Document.create(
            id=DocumentID.from_value(self._id_generator.new_id()),
            collection_file_id=collection_file_id,
            collection_id=collection_id,
            content=result,
            asset_id=asset_id
        )

        await self._document_repo.save(document)

        rag_process.finish_ocr(document.id)
        await self._rag_process_repository.save(rag_process)
