from abc import ABC, abstractmethod
from typing import List

from .strategy import Strategy


class Context:

    def __init__(self, strategy: Strategy = None) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    def parse(self, url: str) -> str:
        return self._strategy.parse(url)
