import os
import time
import logging
import requests
import ptbot
import telegram
from dotenv import load_dotenv


def check_long_polling(timestamp=None):
    logging.debug('Start long polling...')
    api_command = "long_polling"
    payload = {'timestamp': timestamp}  
    try:
        response = requests.get(
            BASE_API_URL + api_command,
            headers=HEADERS,
            params=payload,
        )
        response.raise_for_status()
        if response.ok:
            return response
    except requests.RequestException:
        logging.exception('RequestException')
        return None


if __name__ == "__main__":
    load_dotenv()

    BASE_API_URL = "https://dvmn.org/api/"
    HEADERS = {
        "Authorization": "Token {}".format(os.getenv("DEVMAN_TOKEN")),
    }
    while True:
        while True:
            try:
                bot = ptbot.Bot(os.getenv("TELEGRAM_TOKEN"))
                bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), "Бот запущен...")
                break
            except telegram.error.NetworkError:
                logging.exception('TelegramError')
            time.sleep(60)

        timestamp = None
        try:
            response = check_long_polling(timestamp)
            json_data = response.json()
            if json_data['status'] == 'timeout':
                timestamp = json_data['timestamp_to_request']
            elif json_data['status'] == 'found':
                logging.debug(json_data['new_attempts'][0]['lesson_title'])
                logging.debug(response.url, "\n")

                lesson_title = json_data['new_attempts'][0]['lesson_title']
                score = json_data['new_attempts'][0]['is_negative']
                score_message = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                if not score:
                    score_message = "К сожалению в работе нашлись ошибки"
                message = f"У вас проверили работу \"{lesson_title}\"\n\n{score_message}"
                bot.send_message(
                    os.getenv("TELEGRAM_CHAT_ID"),
                    message
                )

        except telegram.error.NetworkError:
            logging.exception('TelegramError')
        except AttributeError:
            logging.exception('BadResponse')

