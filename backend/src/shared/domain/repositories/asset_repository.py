from typing import Any, Optional
from abc import ABC, abstractmethod

from src.shared.domain.entities.asset import Asset
from src.shared.domain.value_objects.asset_id import AssetID


class AssetRepository(ABC):

    @abstractmethod
    async def save(self, data: Asset, conn: Any = None) -> Asset:
        pass

    @abstractmethod
    async def get_by_id(self, id: AssetID) -> Optional[Asset]:
        pass
