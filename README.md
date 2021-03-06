# Dvmn Notification Bot

Телеграм-бот для отправки уведомлений о проверке работ на сайте 
[dvmn.org](https://dvmn.org/modules/)


## Требования
- Для запуска вам понадобится Python 3.6 или выше.
- Токен телеграм-бота (создайте бота через диалог с ботом 
[@BotFather](https://telegram.me/BotFather) и получите токен)
- Персональный [API-токен Девмана](https://dvmn.org/api/docs/)  

## Запуск
- Загрузите код из репозитория
- Создайте файл `.env` в корневой папке и пропишите переменные окружения 
в формате: `ПЕРЕМЕННАЯ=значение`
```
DVMN_API_TOKEN=<api_токен_девмана>
TG_BOT_TOKEN=<токен_телеграм_бота>
TG_CHAT_ID=<ваш_телеграм_id>
```
- Установите зависимости командой:
```shell
pip install -r requirements.txt
```
- Запустите скрипт командой:
```commandline
python main.py
```

## Запуск на локальной машине с помощью Docker

Для запуска следующих команд, [Docker](https://docs.docker.com/get-docker/) должен быть уже установлен.

Для создания образа перейдите в папку скрипта и запустите команду, заменив NAME
произвольным названием:
```commandline
docker build -t NAME
```

Создайте и запустите контейнер следующей командой, заменив NAME на выбранное ранее название и 
указав путь к файлу с переменными окружения (PATH_TO_FILE):
```commandline
docker run --env-file PATH_TO_FILE NAME
```
