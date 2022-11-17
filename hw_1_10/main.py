import os
from dotenv import load_dotenv

from mytgbotlib import TgBot
from hw_1_10.handlers import Handler
from hw_1_10.service import Service

if __name__ == "__main__":
    load_dotenv()
    bot = TgBot(str(os.getenv("TELEGRAM_TOKEN")))
    service = Service()
    handler = Handler(bot, service)
    handler.init_routes()
    bot.run()
