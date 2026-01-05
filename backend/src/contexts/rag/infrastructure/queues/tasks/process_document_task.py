import asyncio

from dependency_injector.wiring import Provide, inject

from src.contexts.rag.infrastructure.queues.celery_app import celery_app
from src.contexts.rag.boot.worker_container import WorkerContainer
from src.contexts.rag.application.commands.process_document_internal.process_document_internal_handler import ProcessDocumentInternalHandler
from src.contexts.rag.application.commands.process_document_internal.process_document_internal_input import ProcessDocumentInternalInput


@celery_app.task(bind=True, name="process_document_task")
@inject
def process_document_task(
    self,
    collection_id,
    collection_file_id,
    rag_process_id,
    process_document_internal_command: ProcessDocumentInternalHandler = Provide[
        WorkerContainer.process_document_internal_command]
):
    try:

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(
            process_document_internal_command.execute(
                ProcessDocumentInternalInput(
                    collection_id=collection_id,
                    collection_file_id=collection_file_id,
                    rag_process_id=rag_process_id
                )
            )
        )

    except Exception as e:
        raise
