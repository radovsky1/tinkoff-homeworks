from typing import Dict

from mytgbotlib import TgBot, MessageHandler

from hw_1_10.service import ServiceInterface


class Handler:
    def __init__(self, bot: TgBot, service: ServiceInterface):
        self._bot = bot
        self._service = service

    def init_routes(self) -> None:
        self._bot.add_handler(MessageHandler(self.get_program_info))

    def get_program_info(self, update: Dict) -> None:
        query = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        self._bot.send_message(
            self._service.get_program_info(query), chat_id, parse_mode="HTML"
        )
