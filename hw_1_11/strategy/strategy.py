from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def parse(self, url: str) -> str:
        pass
