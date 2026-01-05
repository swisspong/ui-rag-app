import asyncio
from src.contexts.rag.domain.services.async_job_dispatcher import AsyncJobDispatcher
from src.contexts.rag.application.commands.process_document.process_document_input import ProcessDocumentInput
from src.shared.domain.services.id_generator import IDGenerator
from src.contexts.rag.domain.repositories.rag_process_repository import RAGProcessRepository
from src.contexts.rag.domain.entities.rag_process import RAGProcess
from src.contexts.rag.domain.value_objects.rag_process_id import RAGProcessID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
from src.contexts.rag.domain.value_objects.collection_file_id import CollectionFileID


class ProcessDocumentHandler:
    def __init__(
        self,
        job_dispatcher: AsyncJobDispatcher,
        id_generator: IDGenerator,
        rag_process_repository: RAGProcessRepository,
    ):
        self._job_dispatcher = job_dispatcher
        self._id_generator = id_generator
        self._rag_process_repository = rag_process_repository

    async def execute(self, input: ProcessDocumentInput) -> None:
        for collection_file_id in input.collection_file_ids:
            # Create value objects
            collection_id = CollectionID.from_value(input.collection_id)
            collection_file_id_vo = CollectionFileID.from_value(
                collection_file_id)

            # Check if RAGProcess already exists for this collection and file
            rag_process = await self._rag_process_repository.get_by_collection_id_and_collection_file_id(
                collection_id,
                collection_file_id_vo
            )

            # If not exists, create a new one
            if not rag_process:
                rag_process_id = RAGProcessID.from_value(
                    self._id_generator.new_id())
                rag_process = RAGProcess.create(
                    rag_process_id,
                    collection_id,
                    collection_file_id_vo
                )
                await self._rag_process_repository.save(rag_process)

            # Dispatch job with rag_process_id
            await self._job_dispatcher.dispatch(
                job_name="process_document_task",
                payload={
                    "collection_id": input.collection_id,
                    "collection_file_id": collection_file_id,
                    "rag_process_id": rag_process.id.value
                }
            )
