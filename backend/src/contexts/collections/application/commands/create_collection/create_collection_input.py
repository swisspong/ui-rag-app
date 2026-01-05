from dataclasses import dataclass
from typing import Optional



@dataclass
class CreateCollectionInput:
    name: str
    description: str