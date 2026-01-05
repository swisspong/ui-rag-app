from typing import Any, Optional

from src.shared.infrastructure.database.asyncpg_connection import AsyncPGConnection
from src.shared.domain.entities.asset import Asset
from src.shared.domain.value_objects.asset_id import AssetID
from src.shared.domain.repositories.asset_repository import AssetRepository
from src.shared.infrastructure.sql.save_asset import SAVE_ASSET
from src.shared.infrastructure.sql.get_asset_by_id import GET_ASSET_BY_ID
from src.shared.infrastructure.errors import (
    DuplicateRecordError,
    QueryFailed,
    DatabaseError
)


class PostgresAssetRepository(AssetRepository):
    def __init__(self, db: AsyncPGConnection):
        self._db = db

    async def save(self, data: Asset, conn: Any = None) -> Asset:
        try:
            await self._db.execute(
                SAVE_ASSET,
                data.id.value,
                data.filename,
                data.content_type,
                data.size,
                conn=conn,
            )
            return data
        except DuplicateRecordError:
            raise
        except DatabaseError as e:
            print(e)
            raise QueryFailed("SAVE_ASSET", e) from e

    async def get_by_id(self, id: AssetID) -> Optional[Asset]:
        try:
            row = await self._db.fetchrow(
                GET_ASSET_BY_ID,
                id.value
            )
            
            if not row:
                return None
            
            return Asset(
                id=AssetID.from_value(row["id"]),
                content_type=row["content_type"],
                filename=row["filename"],
                size=row["size"]
            )

        except DatabaseError as e:
            raise QueryFailed("GET_ASSET_BY_ID", e) from e
