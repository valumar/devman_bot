import os
import requests
import ptbot
from dotenv import load_dotenv
load_dotenv()

BASE_API_URL = "https://dvmn.org/api/"
HEADERS = {
    "Authorization": "Token {}".format(os.getenv("DEVMAN_TOKEN")),
}


def check_user_reviews():
    api_command = "user_reviews"
    response = requests.get(
        BASE_API_URL + api_command,
        headers=HEADERS
    )
    if response.ok:
        return response.json()


def check_long_polling(timestamp=None):
    api_command = "long_polling"
    payload = {'timestamp': timestamp}  
    response = requests.get(
        BASE_API_URL + api_command,
        headers=HEADERS,
        params=payload,
        # timeout=5
    )
    if response.ok:
        return response
    

if __name__ == "__main__":
    
    bot = ptbot.Bot(os.getenv("TELEGRAM_TOKEN"))
    bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), "Бот запущен...")
    
    timestamp = None
    while True:
        try:
            response = check_long_polling()
            if response.json()['status'] == 'timeout':
                timestamp = response.json()['timestamp_to_request']
                response = check_long_polling(timestamp)
            elif response.json()['status'] == 'found':
                print(response.json())
                print(response.json()['new_attempts'][0]['lesson_title'])
                print(response.url, "\n")
                                
                lesson_title = response.json()['new_attempts'][0]['lesson_title']
                score = response.json()['new_attempts'][0]['is_negative']
                score_message = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                if not score:
                    score_message = "К сожалению в работе нашлись ошибки"
                message = f"У вас проверили работу \"{lesson_title}\"\n\n{score_message}"
                bot.send_message(
                    os.getenv("TELEGRAM_CHAT_ID"), 
                    message
                )
          
        except Exception as e:
            print(e)
            pass
