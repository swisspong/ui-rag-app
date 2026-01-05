from typing import BinaryIO
from abc import ABC, abstractmethod


class OCR(ABC):

    @abstractmethod
    async def extract_text(self, stream: BinaryIO) -> str:
        pass
