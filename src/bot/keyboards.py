from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def result_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✏️ Редагувати Markdown", callback_data="edit_markdown"),
            InlineKeyboardButton("📎 Завантажити PDF", callback_data="generate_pdf")
        ],
        [
            InlineKeyboardButton("🚀 Створити нове резюме", callback_data="new_resume")
        ]
    ])


def start_keyboard(resume_exists: bool = False) -> ReplyKeyboardMarkup:
    if resume_exists:
        buttons = ["✏️ Редагувати резюме"]
    else:
        buttons = ["🚀 Створити резюме"]

    return ReplyKeyboardMarkup(
        [[KeyboardButton(text) for text in buttons]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
