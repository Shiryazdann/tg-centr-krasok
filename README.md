# Telegram AI Bot - Центр Красок #1

AI-ассистент для компании "Центр Красок #1" на базе Groq API и Telegram Bot API.

## Возможности

- Автоматические ответы на вопросы о компании, товарах и услугах
- Память диалога (последние 6 сообщений)
- Поддержка русского, казахского и английского языков
- Деплой на Render

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте `.env` файл:
```
TELEGRAM_BOT_TOKEN=your_telegram_token
GROQ_API_KEY=your_groq_api_key
```

4. Запустите бота:
```bash
python bot.py
```

## Деплой на Render

1. Создайте Web Service на Render
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения:
   - `TELEGRAM_BOT_TOKEN`
   - `GROQ_API_KEY`
4. Render автоматически задеплоит бота

## Структура проекта

- `bot.py` - основной файл бота
- `company_data.py` - информация о компании
- `keep_alive.py` - health-check сервер для Render
- `requirements.txt` - зависимости проекта
