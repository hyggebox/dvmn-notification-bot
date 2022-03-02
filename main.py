import requests

from environs import Env
from telegram import Bot


if __name__ == "__main__":
    env = Env()
    env.read_env()

    dvmn_api_token = env("DVMN_API_TOKEN")
    tg_bot_token = env("TG_BOT_TOKEN")
    chat_id = env("CHAT_ID")
    reviews_endpoint = "https://dvmn.org/api/user_reviews/"
    long_polling_endpoint = "https://dvmn.org/api/long_polling/"

    headers = {
        "Authorization": f"Token {dvmn_api_token}"
    }
    params = {
        "timestamp": 0,
    }

    bot = Bot(token=tg_bot_token)

    while True:
        try:
            response = requests.get(long_polling_endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=10)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        else:
            review_response = response.json()
            timestamp = review_response["last_attempt_timestamp"]
            params = {"timestamp": timestamp}

            if review_response["status"] == "found":
                reviewed_lessons = review_response["new_attempts"]
                for lesson in reviewed_lessons:
                    title = lesson["lesson_title"]
                    is_negative = lesson["is_negative"]

                    if is_negative:
                        msg_tail = f"В работе нашлись ошибки 📝"
                    else:
                        msg_tail = f"Преподавателю всё понравилось. Можно " \
                                   f"приступать к следующему уроку! 🔥"

                    bot.send_message(text=f"Работа «{title}» проверена!\n\n{msg_tail}",
                                     chat_id=chat_id)
