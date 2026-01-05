from abc import ABC, abstractmethod

import numpy as np


class Embedding(ABC):

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
        model: str,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> np.ndarray:
        pass
