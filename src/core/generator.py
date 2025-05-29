from openai import OpenAI
from openai._exceptions import RateLimitError
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)



async def generate_resume(data: dict) -> str:
    prompt = f"""
Сформуй українське резюме у форматі Markdown за наступним шаблоном:

# {{Ім'я Прізвище}}

📍 {{Місто}}, Україна  
📧 {{Email}} | 📞 {{Телефон}}  
🔗 {{LinkedIn}} | {{GitHub}}

---

## 🎯 Мета
{{Ціль/позиція}}

---

## 💼 Досвід
**{{Назва посади}}**  
_{{Компанія}}, {{Місто}} — {{Період}}_  
- {{Обов'язки}}

---

## 📚 Освіта
**{{Назва навчального закладу}}**  
_{{Ступінь, роки}}_

---

## 🧠 Навички
- {{Навичка 1}}  
- {{Навичка 2}}  
- …

---

## 🌐 Мови
- {{Мова}} — {{Рівень}}

---

Ось дані для підстановки:
Ім'я: {data.get('name')}
Посада: {data.get('position')}
Освіта: {data.get('education')}
Навички: {data.get('skills')}
Софт-скіли: {data.get('soft_skills')}
Про себе: {data.get('about')}

**Відповідь має бути лише у Markdown-форматі шаблону. Без додаткового тексту.**
**Не використовуй трійні лапки ```. Поверни лише валідний Markdown.**
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
    except RateLimitError:
        print("[⚠️ GPT-4o недоступний, fallback на gpt-3.5-turbo]")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
        except RateLimitError:
            print("[⛔ Вичерпано квоту для обох моделей]")
            return "❌ Немає доступу до моделей OpenAI. Перевірте квоту або API-ключ."

    return response.choices[0].message.content.strip()


# Тестування при запуску напряму
if __name__ == "__main__":
    import asyncio

    test_data = {
        "name": "Іван Петренко",
        "position": "Junior Python Developer",
        "education": "КНУ, Комп'ютерні науки, 2021–2025",
        "skills": "Python, Git, SQL, Flask",
        "soft_skills": "відповідальність, командна робота",
        "about": "Я захоплююсь розробкою ботів та веб-сервісів."
    }

    print("\nТестуємо генерацію GPT (gpt-4o)...")
    print(asyncio.run(generate_resume(test_data)))
