from typing import Optional

import numpy as np
from openai import AsyncOpenAI

from src.contexts.rag.domain.services.embedding import Embedding


class OpenAIEmbedding(Embedding):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize the OpenAIEmbedding service.

        Args:
            api_key: Optional default API key. Can be overridden in the embed method.
            base_url: Optional default base URL for OpenAI-compatible APIs.
                     Can be overridden in the embed method.
            model: Optional default model name. Can be overridden in the embed method.
        """
        self._default_api_key = api_key
        self._default_base_url = base_url
        self._default_model = model

    async def embed(
        self,
        texts: list[str],
        model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> np.ndarray:
        """
        Generate embeddings for a list of texts using OpenAI's API.

        Args:
            texts: List of text strings to embed.
            model: The embedding model to use (e.g., "text-embedding-3-small").
            base_url: Optional base URL for OpenAI-compatible APIs.
                     If not provided, uses the default from constructor or OpenAI's default.
            api_key: Optional API key. If not provided, uses the default from constructor
                    or the OPENAI_API_KEY environment variable.

        Returns:
            numpy.ndarray: A 2D array of embeddings with shape (len(texts), embedding_dim).

        Raises:
            ValueError: If texts list is empty.
            RuntimeError: If the API request fails.
        """
        if not texts:
            raise ValueError("texts list cannot be empty")

        # Use provided values or fall back to defaults
        effective_api_key = api_key if api_key is not None else self._default_api_key
        effective_base_url = base_url if base_url is not None else self._default_base_url
        effective_model = model if model is not None else self._default_model

        if effective_model is None:
            raise ValueError("model must be provided either as parameter or in constructor")

        try:
            # Create async OpenAI client with optional custom configuration
            client = AsyncOpenAI(
                api_key=effective_api_key,
                base_url=effective_base_url,
            )

            # Make embedding request
            response = await client.embeddings.create(
                input=texts,
                model=effective_model,
            )

            # Extract embeddings from response
            embeddings = [item.embedding for item in response.data]

            # Convert to numpy array with shape (len(texts), embedding_dim)
            return np.array(embeddings, dtype=np.float32)

        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}") from e
