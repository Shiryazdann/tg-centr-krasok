# 🚀 Деплой бота на бесплатный сервер (24/7)

Чтобы бот работал круглосуточно без твоего компьютера, нужно задеплоить его на сервер.

## Вариант 1: Render.com (Рекомендуется)

**Преимущества:**
- ✅ Полностью бесплатно
- ✅ Простая настройка через GitHub
- ✅ Автоматический перезапуск при падении
- ✅ Работает 24/7

### Шаг 1: Подготовка проекта

Создадим дополнительные файлы для деплоя.

### Шаг 2: Загрузка на GitHub

1. Создай новый репозиторий на https://github.com/new
2. Назови его, например: `telegram-bot-centr-krasok`
3. Выполни команды:

```bash
cd C:/Users/Shiryazdan/telegram-ai-bot
git init
git add .
git commit -m "Initial commit: Telegram AI bot"
git remote add origin https://github.com/ВАШ_USERNAME/telegram-bot-centr-krasok.git
git push -u origin main
```

### Шаг 3: Деплой на Render

1. Зайди на https://render.com и зарегистрируйся (можно через GitHub)
2. Нажми **"New +"** → **"Web Service"**
3. Подключи свой GitHub репозиторий
4. Настройки:
   - **Name:** telegram-bot-centr-krasok
   - **Region:** выбери ближайший (Frankfurt или Singapore)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** Free

5. Добавь **Environment Variables** (переменные окружения):
   - `TELEGRAM_BOT_TOKEN` = `ваш_токен_от_BotFather`
   - `GROQ_API_KEY` = `ваш_ключ_от_groq`

6. Нажми **"Create Web Service"**

7. Подожди 2-3 минуты пока бот деплоится

8. **Готово!** Бот теперь работает 24/7 на сервере Render.

---

## Вариант 2: PythonAnywhere (Альтернатива)

**Преимущества:**
- ✅ Бесплатно
- ✅ Не требует GitHub
- ✅ Простой веб-интерфейс

### Инструкция:

1. Зайди на https://www.pythonanywhere.com и зарегистрируйся
2. Открой **"Files"** и загрузи все файлы проекта
3. Открой **"Consoles"** → **"Bash"**
4. Установи зависимости:
   ```bash
   pip install --user -r requirements.txt
   ```
5. Создай файл `.env` с токенами
6. Запусти бота:
   ```bash
   python bot.py &
   ```

---

## Вариант 3: Railway.app

1. Зайди на https://railway.app
2. Подключи GitHub репозиторий
3. Добавь переменные окружения
4. Деплой автоматически начнется

---

## ⚠️ Важно для бесплатных серверов

**Render.com:**
- Бесплатный план засыпает после 15 минут неактивности
- Решение: использовать UptimeRobot (https://uptimerobot.com) для пинга каждые 5 минут

**PythonAnywhere:**
- Нужно перезапускать бота раз в 3 месяца

---

## 🔧 Проверка работы

После деплоя:
1. Открой Telegram
2. Найди своего бота
3. Напиши сообщение
4. Бот должен ответить (даже если твой компьютер выключен!)

---

## 📊 Мониторинг

**Render Dashboard:** https://dashboard.render.com
- Логи бота в реальном времени
- Статус работы
- Использование ресурсов

**UptimeRobot (опционально):**
- Создай монитор для URL вашего сервиса на Render
- Проверка каждые 5 минут
- Email уведомления при падении
