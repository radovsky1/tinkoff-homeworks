import logging
import requests

from typing import Optional, Dict, List
from .handlers import Handler


class TgBotConstants(object):
    BASE_URL = "https://api.telegram.org/bot{}/"
    UPDATES_TIMEOUT = 100

    def __init__(self, token: str):
        self.token = token
        self.base_url = self.BASE_URL.format(self.token)

    def get_updates_endpoint(self, offset=None) -> str:
        url = self.base_url + "getUpdates?timeout={}".format(
            self.UPDATES_TIMEOUT
        )
        if offset:
            url += "&offset={}".format(offset)
        return url

    def send_message_endpoint(self, parse_mode=None) -> str:
        url = self.base_url + "sendMessage?text={}&chat_id={}"
        if parse_mode:
            url += "&parse_mode={}".format(parse_mode)
        return url


class TgBot:
    def __init__(self, token: str):
        self.token = token
        self._constants = TgBotConstants(token)
        self._logger = logging.getLogger(__name__)
        self._handlers: List[Handler] = []
        self._is_running = True

    def _fetch(
        self, url: str, params: dict = None
    ) -> Optional[requests.Response]:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self._logger.error("Request failed: {}".format(e))
            return None
        except requests.exceptions.ConnectionError as e:
            self._logger.error("Request failed: {}".format(e))
            return None
        except requests.exceptions.Timeout as e:
            self._logger.error("Request failed: {}".format(e))
            return None
        except requests.exceptions.RequestException as e:
            self._logger.error("Request failed: {}".format(e))
            return None
        return response

    def _fetch_json(self, url: str, params: dict = None) -> Optional[dict]:
        response = self._fetch(url, params)
        if response is None:
            return None
        return response.json()

    def _get_updates(self, offset=None):
        url = self._constants.get_updates_endpoint(offset)
        return self._fetch_json(url)

    @staticmethod
    def _get_last_update_id(updates: Dict) -> int:
        if not updates:
            return 0
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    @staticmethod
    def _validate(html: str) -> str:
        html = html.replace("<p>", "")
        html = html.replace("</p>", "")
        return html

    def send_message(self, text: str, chat_id: int, parse_mode=None) -> None:
        url = self._constants.send_message_endpoint(parse_mode)

        if parse_mode == "HTML":
            text = self._validate(text)

        url = url.format(text, chat_id)
        self._fetch(url)

    def add_handler(self, handler: Handler) -> None:
        self._handlers.append(handler)

    def _handle_update(self, update: Dict) -> None:
        for handler in self._handlers:
            try:
                handler.handle(update)
            except ValueError as e:
                self._logger.error("Handler failed: {}".format(e))

    def stop(self) -> None:
        self._is_running = False

    def run(self) -> None:
        last_update_id = 0
        while self._is_running:
            updates = self._get_updates(last_update_id)
            if updates and "result" in updates:
                for update in updates["result"]:
                    self._handle_update(update)
                last_update_id = self._get_last_update_id(updates) + 1
