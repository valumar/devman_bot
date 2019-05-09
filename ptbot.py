import logging
import telegram

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class Bot():

    def __init__(self, api_key):
        if not api_key:
            raise(ValueError("Токен не указан"))
        self.api_key = api_key
        self.bot = telegram.Bot(token=api_key)
        self.logger = logging.getLogger('tbot')
        self.updater = Updater(self.api_key)
        self.dispatcher = self.updater.dispatcher
        self.logger.debug('Bot initialized')

    def send_message(self, chat_id, message):
        self.logger.debug(f'Message send: {message}')
        return self.bot.send_message(chat_id=chat_id, text=message).message_id

    def update_message(self, chat_id, message_id, new_message):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_message)
        self.logger.debug(f'Update message {message_id}: {new_message}')

    def wait_for_msg(self, callback):
        if not callable(callback):
            raise TypeError('Ожидаем функцию на вход')

        def handle_text(bot, update):
            users_reply = update.message.text
            callback(users_reply)

        self.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
        self.updater.start_polling()
        self.updater.idle()
