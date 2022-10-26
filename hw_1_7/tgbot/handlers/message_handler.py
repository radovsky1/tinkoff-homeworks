from typing import Callable

from .handler import Handler


class MessageHandler(Handler):
    def __init__(self, callback: Callable):
        super().__init__(callback)

    def handle(self, update):
        if update.get("message") is not None:
            if update["message"].get("text") is not None and not update[
                "message"
            ]["text"].startswith("/"):
                super().handle(update)
            else:
                raise ValueError("Message has no text")
