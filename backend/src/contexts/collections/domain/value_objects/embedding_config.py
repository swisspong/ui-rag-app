from dataclasses import dataclass
from typing import Optional

from ..errors.invalid_embedding_config import InvalidEmbeddingConfig

@dataclass(frozen=True)
class EmbeddingConfig:
    _model: str
    _base_url: Optional[str]
    _api_key: str

    @staticmethod
    def from_value(model: str, api_key: str, base_url: Optional[str] = None) -> "EmbeddingConfig":
        if not model or not model.strip():
            raise InvalidEmbeddingConfig("model name cannot be empty")

        if not api_key or not api_key.strip():
            raise InvalidEmbeddingConfig("API Key cannot be empty.")

        return EmbeddingConfig(
            _model=model.strip(),
            _base_url=base_url.strip() if base_url else None,
            _api_key=api_key.strip()
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def base_url(self) -> Optional[str]:
        return self._base_url

    @property
    def api_key(self) -> str:
        return self._api_key
