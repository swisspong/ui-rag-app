from abc import ABC, abstractmethod
from typing import BinaryIO

from src.shared.domain.entities.asset import Asset
from src.shared.domain.value_objects.asset_id import AssetID


class AssetStorage(ABC):
    @abstractmethod
    async def save(
        self,
        asset: Asset,
        content: BinaryIO,
    ) -> None:
        pass

    @abstractmethod
    async def open(
        self,
        file_id: AssetID,
    ) -> BinaryIO:
        pass
