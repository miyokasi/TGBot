# README.md

# 🤖 ResumeBot — Telegram-бот для генерації резюме на основі GPT

Цей бот дозволяє користувачу покроково ввести свої дані та отримати згенероване резюме у вигляді тексту та (опціонально) PDF.

---

## 🚀 Швидкий старт для клієнта

### 1. Створіть Telegram-бота
1. Відкрийте [@BotFather](https://t.me/BotFather)
2. Надішліть команду `/newbot`
3. Дайте ім’я та юзернейм (має закінчуватись на `bot`)
4. Скопіюйте отриманий токен (він виглядає як `123456:ABC-DEF...`)

### 2. Отримайте OpenAI API ключ
1. Перейдіть на [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Зареєструйтесь або увійдіть
3. Натисніть "Create new secret key"
4. Скопіюйте ключ (починається з `sk-...`)

### 3. Заповніть `.env` файл:
Створіть файл `.env` в корені проєкту:
```env
BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_key
```

### 4. Запустіть проєкт локально:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

> ❗ Переконайтесь, що Python 3.8 або новіший

---

## 📁 Структура проєкту
```
resume-bot/
├── src/
│   ├── bot/              # Telegram логіка
│   ├── core/             # GPT-генерація, конфіг, PDF
│   └── __init__.py
├── .env                 # Секрети (не пушити!)
├── main.py              # Точка входу
├── requirements.txt     # Залежності
└── README.md            # Інструкція
```

---

## 📦 Деплой на Railway (опціонально)
1. Створи акаунт: [https://railway.app](https://railway.app)
2. Створи новий проєкт → "Deploy from GitHub"
3. У вкладці Variables додай `BOT_TOKEN` і `OPENAI_API_KEY`
4. Railway сам запустить `main.py`

---

## 📬 Підтримка
З усіх питань звертайтесь до розробника або через Telegram: `@miyokasi`


