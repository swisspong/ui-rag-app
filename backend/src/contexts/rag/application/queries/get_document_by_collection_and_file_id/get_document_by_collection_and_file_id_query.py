from typing import Optional

from src.contexts.rag.application.queries.get_document_by_collection_and_file_id.get_document_by_collection_and_file_id_input import GetDocumentByCollectionAndFileIdInput
from src.contexts.rag.application.queries.repoistories.document_read_repository import DocumentReadRepository
from src.contexts.rag.application.queries.models.document_read_model import DocumentReadModel


class GetDocumentByCollectionAndFileIdQuery:
    def __init__(
        self,
        document_read_repository: DocumentReadRepository
    ):
        self._document_read_repo = document_read_repository

    async def execute(self, input: GetDocumentByCollectionAndFileIdInput) -> Optional[DocumentReadModel]:
        document = await self._document_read_repo.get_by_collection_and_file_id(
            input.collection_id,
            input.collection_file_id
        )
        return document
