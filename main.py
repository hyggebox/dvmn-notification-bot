import logging
import requests

from environs import Env
from telegram import Bot
from time import sleep


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(level=logging.DEBUG)

    dvmn_api_token = env("DVMN_API_TOKEN")
    tg_bot_token = env("TG_BOT_TOKEN")
    tg_chat_id = env("TG_CHAT_ID")
    long_polling_endpoint = "https://dvmn.org/api/long_polling/"

    headers = {
        "Authorization": f"Token {dvmn_api_token}"
    }
    params = {
        "timestamp": 0,
    }

    bot = Bot(token=tg_bot_token)

    while True:
        logging.info("Бот запущен")
        try:
            response = requests.get(long_polling_endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=10)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            sleep(60)
        else:
            review_response = response.json()
            if review_response["status"] == "timeout":
                timestamp = review_response["timestamp_to_request"]

            elif review_response["status"] == "found":
                timestamp = review_response["last_attempt_timestamp"]
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
                                     chat_id=tg_chat_id)

            params = {"timestamp": timestamp}
