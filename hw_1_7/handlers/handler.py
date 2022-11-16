from hw_1_7.tgbot import TgBot, CommandHandler, MessageHandler
from hw_1_7.service import ServiceInterface

from typing import Dict


class Routes(object):
    """Class that contains all routes."""

    ADD_TO_FAVORITES = "/add_to_favorites"
    REMOVE_FROM_FAVORITES = "/remove_from_favorites"
    GET_FAVORITES = "/get_favorites"


class Handler:
    def __init__(self, bot: TgBot, service: ServiceInterface):
        self._bot = bot
        self._service = service

    def init_routes(self) -> None:
        self._bot.add_handler(MessageHandler(self.get_program_info))
        self._bot.add_handler(
            CommandHandler(self.add_to_favorites, Routes.ADD_TO_FAVORITES)
        )
        self._bot.add_handler(
            CommandHandler(
                self.remove_from_favorites, Routes.REMOVE_FROM_FAVORITES
            )
        )
        self._bot.add_handler(
            CommandHandler(self.get_favorites, Routes.GET_FAVORITES)
        )

    def get_program_info(self, update: Dict) -> None:
        query = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        self._bot.send_message(
            self._service.get_program_info(query), chat_id, parse_mode="HTML"
        )

    def add_to_favorites(self, update: Dict) -> None:
        query = update["message"]["text"].replace(Routes.ADD_TO_FAVORITES, "")
        chat_id = update["message"]["chat"]["id"]
        self._bot.send_message(
            self._service.add_to_favorites(query), chat_id, parse_mode="HTML"
        )

    def remove_from_favorites(self, update: Dict) -> None:
        query = update["message"]["text"].replace(
            Routes.REMOVE_FROM_FAVORITES, ""
        )
        chat_id = update["message"]["chat"]["id"]
        self._bot.send_message(
            self._service.remove_from_favorites(query),
            chat_id,
            parse_mode="HTML",
        )

    def get_favorites(self, update: Dict) -> None:
        chat_id = update["message"]["chat"]["id"]
        self._bot.send_message(
            self._service.get_favorites(), chat_id, parse_mode="HTML"
        )
