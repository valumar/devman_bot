# Inspired by RealPython: https://realpython.com/python-logging/

import os
import logging
import logging.handlers
import requests
import telegram

from time import sleep

from dotenv import load_dotenv
load_dotenv()


class TelegramBotHandler(logging.Handler):
    def __init__(self, telegram_api_token, telegram_chat_id):
        super().__init__()
        self.telegram_chat_id = telegram_chat_id
        self.bot = telegram.Bot(telegram_api_token)

    def emit(self, record):
        while True:
            try:
                logger.removeHandler(self)
                url = "https://api.telegram.org/"
                response = requests.get(url)
                if response.ok:
                    logger.addHandler(self)
                msg = self.format(record)
                chunks, chunk_size = len(msg), telegram.constants.MAX_MESSAGE_LENGTH
                chunked_msg = [msg[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
                for chunk in chunked_msg:
                    self.bot.send_message(self.telegram_chat_id, chunk, timeout=10)
                    sleep(1)
                break
            except Exception as e:
                logger.exception("Exception in TelegramBotHandler")
                sleep(10)


# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# bot_logger.addFilter(NoTelegramFilter())

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=1024 * 1000, backupCount=5)

c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log_format = logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


bot_handler = TelegramBotHandler(os.getenv("TELEGRAM_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
bot_handler.setLevel(logging.INFO)
# bot_handler.setFormatter(log_format)
logger.addHandler(bot_handler)
