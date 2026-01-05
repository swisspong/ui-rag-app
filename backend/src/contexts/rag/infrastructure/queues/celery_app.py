import asyncio
from celery.signals import worker_process_init, worker_process_shutdown
from celery import Celery
from src.contexts.rag.boot.worker_container import WorkerContainer
container: WorkerContainer | None = None
event_loop: asyncio.AbstractEventLoop | None = None
# container = WorkerContainer()

redis_url = f"redis://localhost:6379/0"

celery_app = Celery(
    "rag_process",
    broker=redis_url,
    backend=redis_url,
    include=["src.contexts.rag.infrastructure.queues.tasks.process_document_task"]
)



@worker_process_init.connect
def on_worker_start(**kwargs):
    global container, event_loop

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    container = WorkerContainer()
    # container.config.from_pydantic(Settings())
    container.wire(
        modules=[
            "src.contexts.rag.infrastructure.queues.tasks.process_document_task",
        ]
    )
    database = container.database()
    event_loop.run_until_complete(database.connect())


@worker_process_shutdown.connect
def on_worker_shutdown(**kwargs):
    global container, event_loop

    if container and event_loop:
        database = container.database()
        event_loop.run_until_complete(database.disconnect())

        container.unwire()
        event_loop.close()