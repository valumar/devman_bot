import os
import time
import logging
import requests
import ptbot
import telegram
from dotenv import load_dotenv


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    # filename='log.log'
)


def check_long_polling(base_api_url, headers, timestamp=None):
    logging.debug('Start long polling...')
    api_command = "long_polling"
    payload = {'timestamp': timestamp}  
    response = requests.get(
        base_api_url + api_command,
        headers=headers,
        params=payload,
    )
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    base_api_url = "https://dvmn.org/api/"
    headers = {
        "Authorization": "Token {}".format(os.getenv("DEVMAN_TOKEN")),
    }
    while True:
        while True:
            try:
                bot = ptbot.Bot(os.getenv("TELEGRAM_TOKEN"))
                logging.debug("Бот запущен...")
                break
            except telegram.error.NetworkError:
                logging.exception('TelegramError')
            time.sleep(60)

        timestamp = None
        try:
            json_data = check_long_polling(base_api_url, headers, timestamp)
            if json_data['status'] == 'timeout':
                timestamp = json_data['timestamp_to_request']
            elif json_data['status'] == 'found':
                last_lesson = json_data['new_attempts'][0]
                lesson_title = last_lesson['lesson_title']
                logging.debug(lesson_title)
                logging.debug(last_lesson)
                score = last_lesson['is_negative']
                score_message = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                if score:
                    score_message = "К сожалению в работе нашлись ошибки"
                message = f"У вас проверили работу \"{lesson_title}\"\n\n{score_message}"
                bot.send_message(
                    os.getenv("TELEGRAM_CHAT_ID"),
                    message
                )

        except telegram.error.NetworkError:
            logging.exception('TelegramError')
        except requests.RequestException:
            logging.exception('RequestException')


if __name__ == "__main__":
    main()
