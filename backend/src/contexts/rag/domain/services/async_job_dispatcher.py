from abc import ABC, abstractmethod

class AsyncJobDispatcher(ABC):

    @abstractmethod
    async def dispatch(
        self,
        job_name: str,
        payload: dict
    ) -> None:
        pass
