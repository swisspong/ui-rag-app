from pydantic import BaseModel
from typing import Optional

class EmbeddingSettings(BaseModel):
    model: str
    base_url: Optional[str] = None
    api_key: str
