from typing import Callable


class Handler:
    def __init__(self, callback: Callable):
        self.callback = callback

    def handle(self, update):
        self.callback(update)
