from typing import Callable

from .handler import Handler


class CommandHandler(Handler):
    def __init__(self, callback: Callable, command: str):
        super().__init__(callback)
        self._command = command

    def handle(self, update) -> None:
        if update.get("message") is not None:
            if update["message"].get("text") is not None:
                if update["message"]["text"].startswith(self._command):
                    super().handle(update)
            else:
                raise ValueError("Message has no text")
        else:
            raise ValueError("Update has no message")
