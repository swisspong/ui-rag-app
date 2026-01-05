from typing import List
from abc import ABC, abstractmethod


class Tokenizer(ABC):
    @abstractmethod
    def encode(self, content: str) -> List[int]:
        pass

    @abstractmethod
    def decode(self, tokens: List[int]) -> str:
        pass
