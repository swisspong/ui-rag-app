from abc import ABC, abstractmethod


class IDGenerator(ABC):

    @abstractmethod
    def new_id(self) -> str:
        pass
