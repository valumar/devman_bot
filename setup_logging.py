# Inspired by RealPython: https://realpython.com/python-logging/

import logging
import logging.handlers
import requests
import json
import ptbot
import os
import telegram
from time import sleep


class TelegramBotHandler(logging.Handler):

    def emit(self, record):
        while True:
            try:
                msg = self.format(record)
                url = "https://api.telegram.org/bot"
                token = os.getenv("TELEGRAM_TOKEN")
                api_command = "/sendMessage"
                headers = {'content-type': 'application/json'}
                payload = {
                    "chat_id": f'{os.getenv("TELEGRAM_CHAT_ID")}',
                    "text": f'{msg}'
                }
                response = requests.post(
                    f"{url}{token}{api_command}",
                    headers=headers,
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                break
            except Exception as e:
                logger.removeHandler(self)
                logger.exception("Exception in TelegramBotHandler")
                logger.addHandler(self)
                sleep(10)

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=20480, backupCount=5)

c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
log_format = logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

bot_handler = TelegramBotHandler()
bot_handler.setLevel(logging.INFO)
# bot_handler.setFormatter(log_format)
logger.addHandler(bot_handler)
