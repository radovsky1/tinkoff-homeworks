import threading
import time

from hw_1_7.tgbot import TgBot, CommandHandler, MessageHandler


def test_add_handler():
    def start(update):
        pass

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    tgbot.add_handler(CommandHandler(start, "/start"))

    assert len(tgbot._handlers) == 1


def test_send_message(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage?text=Hello&chat_id=1",
        json={"ok": True, "result": {"message_id": 1, "chat": {"id": 1}}},
    )

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    tgbot.send_message("Hello", 1)

    assert requests_mock.called


def test_get_updates(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={
            "result": [
                {
                    "update_id": 1,
                    "message": {
                        "message_id": 1,
                        "from": {
                            "id": 1,
                            "is_bot": False,
                            "first_name": "John",
                        },
                        "chat": {
                            "id": 1,
                            "first_name": "John",
                            "type": "private",
                        },
                        "date": 1610071499,
                        "text": "Hello",
                    },
                }
            ],
        },
    )

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    updates = tgbot._get_updates()

    assert len(updates["result"]) == 1


def test_get_empty_updates(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={"result": []},
    )

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    updates = tgbot._get_updates()

    assert len(updates["result"]) == 0


def test_get_last_update_id(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={
            "result": [
                {
                    "update_id": 1,
                    "message": {
                        "message_id": 1,
                        "from": {
                            "id": 1,
                            "is_bot": False,
                            "first_name": "John",
                        },
                        "chat": {
                            "id": 1,
                            "first_name": "John",
                            "type": "private",
                        },
                        "date": 1610071499,
                        "text": "Hello",
                    },
                },
                {
                    "update_id": 2,
                    "message": {
                        "message_id": 2,
                        "from": {
                            "id": 1,
                            "is_bot": False,
                            "first_name": "John",
                        },
                        "chat": {
                            "id": 1,
                            "first_name": "John",
                            "type": "private",
                        },
                        "date": 1610071499,
                        "text": "Hello",
                    },
                },
            ],
        },
    )

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    updates = tgbot._get_updates()

    assert tgbot._get_last_update_id(updates) == 2


def test_command_handler(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={
            "ok": True,
            "result": [
                {
                    "update_id": 1,
                    "message": {
                        "message_id": 1,
                        "from": {
                            "id": 1,
                            "is_bot": False,
                            "first_name": "John",
                        },
                        "chat": {
                            "id": 1,
                            "first_name": "John",
                            "type": "private",
                        },
                        "date": 1610071499,
                        "text": "/start",
                    },
                }
            ],
        },
    )

    def start(update):
        pass

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    tgbot.add_handler(CommandHandler(start, "/start"))

    thread = threading.Thread(target=tgbot.run)
    thread.start()
    time.sleep(0.1)

    tgbot.stop()

    assert requests_mock.called


def test_message_handler(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={
            "ok": True,
            "result": [
                {
                    "update_id": 1,
                    "message": {
                        "message_id": 1,
                        "from": {
                            "id": 1,
                            "is_bot": False,
                            "first_name": "John",
                        },
                        "chat": {
                            "id": 1,
                            "first_name": "John",
                            "type": "private",
                        },
                        "date": 1610071499,
                        "text": "Hello",
                    },
                }
            ],
        },
    )

    def echo(update):
        pass

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    tgbot.add_handler(MessageHandler(echo))

    thread = threading.Thread(target=tgbot.run)
    thread.start()
    time.sleep(0.1)

    tgbot.stop()

    assert requests_mock.called


def test_validate_html():
    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")

    text = "<p>Test</p>"
    assert tgbot._validate(text) == "Test"


def test_get_updates_with_error(requests_mock):
    requests_mock.get(
        "https://api.telegram.org/bot1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getUpdates?timeout=100",
        json={
            "ok": False,
            "error_code": 400,
            "description": "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 5",
        },
    )

    tgbot = TgBot("1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    updates = tgbot._get_updates()

    assert "result" not in updates
