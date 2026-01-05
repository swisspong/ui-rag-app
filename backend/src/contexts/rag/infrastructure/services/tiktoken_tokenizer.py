from typing import List
from src.contexts.rag.domain.services.tokenizer import Tokenizer


class TiktokenTokenizer(Tokenizer):
    def __init__(self):
        model_name = "gpt-4o-mini"
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "tiktoken is not installed. Please install it with `pip install tiktoken` or define custom `tokenizer_func`."
            )

        try:
            self.tokenizer = tiktoken.encoding_for_model(model_name)
        except KeyError:
            raise ValueError(f"Invalid model_name: {model_name}.")

    def decode(self, tokens: List[int]) -> str:
        return self.tokenizer.decode(tokens)

    def encode(self, content: str) -> List[int]:
        return self.tokenizer.encode(content)
