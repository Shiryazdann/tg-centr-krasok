import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI
from company_data import COMPANY_INFO

try:
    from keep_alive import start_health_server_background
    KEEP_ALIVE_ENABLED = True
except ImportError:
    KEEP_ALIVE_ENABLED = False

load_dotenv()

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
    print("=== Starting Telegram Bot ===")
    print(f"Python version: {os.sys.version}")
    print(f"TELEGRAM_TOKEN present: {bool(TELEGRAM_TOKEN)}")
    print(f"GROQ_API_KEY present: {bool(GROQ_API_KEY)}")
    print(f"Keep-alive enabled: {KEEP_ALIVE_ENABLED}")

    if not TELEGRAM_TOKEN:
        print("ОШИБКА: Установите переменную окружения TELEGRAM_BOT_TOKEN")
        return

    if not GROQ_API_KEY:
        print("ОШИБКА: Установите переменную окружения GROQ_API_KEY")
        return

    if KEEP_ALIVE_ENABLED:
        start_health_server_background()
        print("Keep-alive server started for cloud deployment")

    print("Building application...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    print("Adding handlers...")
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot zapuschen i gotov k rabote!")
    print("Nazhmite Ctrl+C dlya ostanovki")

    print("Starting polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
