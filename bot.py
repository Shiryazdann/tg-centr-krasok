#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("Starting bot.py imports...", flush=True)

import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

print("Loading .env...", flush=True)
from dotenv import load_dotenv
load_dotenv()

print("Importing Telegram libraries...", flush=True)
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

print("Importing OpenAI...", flush=True)
from openai import OpenAI

print("Importing company data...", flush=True)
from company_data import COMPANY_INFO

print("Importing keep_alive...", flush=True)
from keep_alive import start_health_server_background
KEEP_ALIVE_ENABLED = True

print("All imports successful!", flush=True)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

user_conversations = defaultdict(lambda: {"messages": [], "last_activity": datetime.now()})

MAX_HISTORY = 6  

SYSTEM_PROMPT = f"""Ты - вежливый и профессиональный AI-ассистент компании "Центр Красок #1".

Твоя задача - отвечать на вопросы клиентов о компании, товарах и услугах на основе предоставленной информации.

ВАЖНЫЕ ПРАВИЛА:
1. Отвечай ТОЛЬКО на основе информации ниже. Не придумывай факты.
2. Если информации нет в базе знаний - честно скажи об этом и предложи связаться с менеджером.
3. Будь дружелюбным, но профессиональным.
4. Отвечай на языке вопроса (русский/казахский/английский).
5. Если вопрос не связан с компанией - вежливо напомни, что ты помогаешь только по вопросам о Центре Красок.

ИНФОРМАЦИЯ О КОМПАНИИ:
{COMPANY_INFO}

При упоминании контактов всегда предоставляй полную информацию (телефоны, адреса, время работы).
"""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка входящих сообщений с памятью диалога"""
    user_message = update.message.text
    user_id = update.effective_user.id

    await update.message.chat.send_action(action="typing")

    try:
        current_time = datetime.now()
        if current_time - user_conversations[user_id]["last_activity"] > timedelta(minutes=30):
            user_conversations[user_id]["messages"] = []

        user_conversations[user_id]["last_activity"] = current_time

        user_conversations[user_id]["messages"].append(
            {"role": "user", "content": user_message}
        )

        history = user_conversations[user_id]["messages"][-MAX_HISTORY:]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content

        user_conversations[user_id]["messages"].append(
            {"role": "assistant", "content": bot_reply}
        )

        await update.message.reply_text(bot_reply)

    except Exception as e:
        error_message = (
            "Извините, произошла ошибка при обработке вашего запроса. "
            "Пожалуйста, попробуйте позже или свяжитесь с нами по телефону: +7 (777) 292-84-01"
        )
        await update.message.reply_text(error_message)
        print(f"Ошибка: {e}")


def main():
    print("=== Starting Telegram Bot ===", flush=True)
    print(f"Python version: {sys.version}", flush=True)

    # Запускаем health-check сервер ПЕРВЫМ для Render
    if KEEP_ALIVE_ENABLED:
        print("Starting health-check server...", flush=True)
        start_health_server_background()
        print("Health-check server started on port 8080", flush=True)

    print(f"TELEGRAM_TOKEN present: {bool(TELEGRAM_TOKEN)}", flush=True)
    print(f"GROQ_API_KEY present: {bool(GROQ_API_KEY)}", flush=True)

    if not TELEGRAM_TOKEN:
        print("ОШИБКА: Установите переменную окружения TELEGRAM_BOT_TOKEN", flush=True)
        return

    if not GROQ_API_KEY:
        print("ОШИБКА: Установите переменную окружения GROQ_API_KEY", flush=True)
        return

    print("Building application...", flush=True)
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    print("Adding handlers...", flush=True)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot zapuschen i gotov k rabote!", flush=True)
    print("Nazhmite Ctrl+C dlya ostanovki", flush=True)

    print("Starting polling...", flush=True)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        print("=== __main__ started ===", flush=True)
        main()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
