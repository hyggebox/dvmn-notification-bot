import logging
import requests

from environs import Env
from telegram import Bot
from time import sleep


logger = logging.getLogger("Logger")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    dvmn_api_token = env("DVMN_API_TOKEN")
    tg_bot_token = env("TG_BOT_TOKEN")
    tg_chat_id = env("TG_CHAT_ID")
    long_polling_endpoint = "https://dvmn.org/api/long_polling/"

    bot = Bot(token=tg_bot_token)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    logger.info("Бот запущен")

    headers = {
        "Authorization": f"Token {dvmn_api_token}"
    }
    params = {
        "timestamp": 0,
    }

    while True:
        try:
            response = requests.get(long_polling_endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=60)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logger.error("⚠ Ошибка бота: ConnectionError")
            sleep(60)
        except Exception as err:
            logger.exception(f"⚠ Ошибка бота:\n\n {err}")
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
