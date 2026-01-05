from typing import BinaryIO
from abc import ABC, abstractmethod

from src.shared.domain.entities.asset import Asset


class OCR(ABC):

    @abstractmethod
    async def extract_text(self, asset: Asset, stream: BinaryIO) -> str:
        pass
