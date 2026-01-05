from celery import Celery
from src.contexts.rag.domain.services.async_job_dispatcher import AsyncJobDispatcher


class CeleryAsyncDispatcher(AsyncJobDispatcher):
    def __init__(
        self, 
        celery_app: Celery
    ):
        self._celery_app = celery_app

    async def dispatch(
        self,
        job_name: str,
        payload: dict
    ) -> None:

        self._celery_app.send_task(
            job_name,
            args=[*payload.values()],
        )
