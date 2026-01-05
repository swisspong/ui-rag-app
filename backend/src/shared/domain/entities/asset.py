from src.shared.domain.value_objects.asset_id import AssetID
from dataclasses import dataclass

@dataclass(frozen=True)
class Asset:
    id: AssetID
    filename: str
    content_type: str
    size: int

    @staticmethod
    def create(
        id: AssetID,
        filename: str,
        content_type: str,
        size: int,
    ) -> "Asset":
        return Asset(
            id=id,
            filename=filename,
            content_type=content_type,
            size=size
        )

    # def mark_processing(self):
    #     if self.status != FileStatus.UPLOADED:
    #         raise ValueError("File is not in UPLOADED state")
    #     self.status = FileStatus.PROCESSING

    # def mark_processed(self):
    #     self.status = FileStatus.PROCESSED

    # def mark_failed(self):
    #     self.status = FileStatus.FAILED
