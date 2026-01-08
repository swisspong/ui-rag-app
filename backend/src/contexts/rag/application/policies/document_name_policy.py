from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.repositories.document_repository import DocumentRepository


class DocumentNamePolicy:
    def __init__(
        self,
        document_repository: DocumentRepository
    ):
        self._document_repo = document_repository

    async def resolve(
        self,
        collection_id: CollectionID,
        filename: str
    ) -> str:
        documents = await self._document_repo.get_many_by_collection_id(collection_id)

        # Extract names from documents. Assuming Document entity has a name field of type DocumentName
        existing_names = {doc.name.value for doc in documents}

        if filename not in existing_names:
            return filename

        if "." in filename:
            base, ext = filename.rsplit(".", 1)
            ext = "." + ext
        else:
            base, ext = filename, ""

        counter = 1
        while True:
            candidate = f"{base} ({counter}){ext}"
            if candidate not in existing_names:
                return candidate
            counter += 1
