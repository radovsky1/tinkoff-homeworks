import os
from dotenv import load_dotenv

from hw_1_7.tgbot import TgBot, MessageHandler
from hw_1_7.tvmaze import search


def _fetch_program_info(program_name):
    try:
        program = search(program_name)
    except ValueError:
        return "Bad request"
    if program is None:
        return "No results found"
    return (
        "Name: {}\n"
        "Network Name: {}\n"
        "Network Country Name: {}\n"
        "Summary: {}".format(
            program.name,
            program.network.name,
            program.network.country.name,
            program.summary,
        )
    )


def handler(update):
    query = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    bot.send_message(_fetch_program_info(query), chat_id, parse_mode="HTML")


if __name__ == "__main__":
    load_dotenv()
    bot = TgBot(str(os.getenv("TELEGRAM_TOKEN")))
    bot.add_handler(MessageHandler(handler))
    bot.run()
