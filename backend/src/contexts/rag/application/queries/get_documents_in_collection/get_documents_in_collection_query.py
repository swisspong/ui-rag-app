from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_input import GetDocumentsInCollectionInput
from src.contexts.rag.application.queries.get_documents_in_collection.get_documents_in_collection_output import GetDocumentsInCollectionOutput
from src.contexts.rag.application.queries.repoistories.document_read_repository import DocumentReadRepository


class GetDocumentsInCollectionQuery:
    def __init__(
        self,
        document_read_repository: DocumentReadRepository
    ):
        self._document_read_repo = document_read_repository

    async def execute(self, input: GetDocumentsInCollectionInput) -> GetDocumentsInCollectionOutput:
        documents = await self._document_read_repo.get_by_collection_id(input.collection_id)
        return GetDocumentsInCollectionOutput(
            documents=documents
        )
