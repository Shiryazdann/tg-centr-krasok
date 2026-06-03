import os
from dotenv import load_dotenv
from openai import OpenAI
from company_data import COMPANY_INFO

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv('GROQ_API_KEY')
)

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

def test_question(question):
    """Тестирование ответа на вопрос"""
    print(f"\n{'='*60}")
    print(f"ВОПРОС: {question}")
    print(f"{'='*60}")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=800,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        print(f"\nОТВЕТ:\n{answer}\n")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    test_questions = [
        "Чем занимается компания?",
        "Какие краски вы продаете?",
        "Где находится ваш офис?",
        "Как с вами связаться?",
        "Сколько оттенков красок доступно?",
        "Какой у вас режим работы?",
        "Можно ли заказать доставку?",
        "Какие бренды у вас есть?",
    ]

    print("🧪 ТЕСТИРОВАНИЕ AI-АССИСТЕНТА")
    print("=" * 60)

    for question in test_questions:
        test_question(question)
        input("\nНажмите Enter для следующего вопроса...")
