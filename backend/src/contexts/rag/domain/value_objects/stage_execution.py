from enum import Enum

class ProcessStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"

class ProcessStage(str, Enum):
    OCR = "ocr"
    INGEST = "ingest"
    CHUNKING = "chunking"
    
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class StageExecution:
    status: ProcessStatus
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    @staticmethod
    def pending():
        return StageExecution(
            status=ProcessStatus.PENDING,
            started_at=None,
            finished_at=None,
        )

    def start(self, now: datetime):
        return StageExecution(
            status=ProcessStatus.RUNNING,
            started_at=now,
            finished_at=None,
        )

    def finish(self, now: datetime):
        return StageExecution(
            status=ProcessStatus.COMPLETED,
            started_at=self.started_at,
            finished_at=now,
        )

    def fail(self, now: datetime):
        return StageExecution(
            status=ProcessStatus.FAILED,
            started_at=self.started_at,
            finished_at=now,
        )
