import os
import time
import logging
import requests
import ptbot
import telegram
from dotenv import load_dotenv
import setup_logging

logger = logging.getLogger(__name__)


def check_long_polling(base_api_url, headers, timestamp=None):
    logger.info('Start long polling...')
    api_command = "long_polling"
    payload = {'timestamp': timestamp}
    response = requests.get(
        base_api_url + api_command,
        headers=headers,
        params=payload,
        timeout=91
    )
    response.raise_for_status()
    return response.json()


def main():
    base_api_url = "https://dvmn.org/api/"
    headers = {
        "Authorization": "Token {}".format(os.getenv("DEVMAN_TOKEN")),
    }
    while True:
        while True:
            try:
                bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
                logger.info("Бот запущен...")
                break
            except telegram.error.NetworkError:
                logger.exception('TelegramError')
            time.sleep(60)

        timestamp = None
        try:
            json_data = check_long_polling(base_api_url, headers, timestamp)
            if json_data['status'] == 'timeout':
                timestamp = json_data['timestamp_to_request']
            elif json_data['status'] == 'found':
                last_lesson = json_data['new_attempts'][0]
                lesson_title = last_lesson['lesson_title']
                logger.debug(lesson_title)
                logger.debug(last_lesson)
                score = last_lesson['is_negative']
                score_message = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                if score:
                    score_message = "К сожалению в работе нашлись ошибки"
                message = f"У вас проверили работу \"{lesson_title}\"\n\n{score_message}"
                bot.send_message(
                    os.getenv("TELEGRAM_CHAT_ID"),
                    message
                )

        except requests.exceptions.ReadTimeout:
            logger.exception('ReadTimeout')
        except telegram.error.NetworkError:
            logger.exception('TelegramError')
        except requests.RequestException as requests_error:
            logger.exception('RequestException')
        except Exception:
            logger.exception('UnknownException')


if __name__ == "__main__":
    load_dotenv()
    setup_logging.config_logging(os.getenv("TELEGRAM_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))
    main()
