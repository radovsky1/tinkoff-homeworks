import os
from dotenv import load_dotenv

from hw_1_7.tgbot import TgBot
from hw_1_7.handlers import Handler
from hw_1_7.service import Service
from hw_1_7.filedict import FileDict

if __name__ == "__main__":
    load_dotenv()
    bot = TgBot(str(os.getenv("TELEGRAM_TOKEN")))
    favorites = FileDict("favorites")
    service = Service(favorites)
    handler = Handler(bot, service)
    handler.init_routes()
    bot.run()
