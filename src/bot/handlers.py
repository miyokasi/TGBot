import os

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.bot.keyboards import result_keyboard, start_keyboard
from src.bot.states import *
from src.core.config import logger
from src.core.generator import generate_resume
from src.core.pdf_generator import generate_pdf


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Користувач %s натиснув /start", update.effective_user.id)

    message = update.message or update.callback_query.message
    user_firstname = update.effective_user.first_name or "👤"
    resume_exists = context.user_data.get("resume") is not None

    if resume_exists:
        text = (
            f"👋 Привіт знову, {user_firstname}!\n\n"
            "📄 Ти вже створив резюме. Обери дію нижче:"
        )

        await message.reply_text(
            text,
            reply_markup=result_keyboard()  # інлайн-кнопки: редагувати / PDF / нове резюме
        )
        return end()

    else:
        text = (
            f"👋 Привіт, {user_firstname}!\n\n"
            "Я — бот, який допоможе тобі згенерувати професійне резюме ✨\n\n"
            "Вибери дію нижче:"
        )

        await message.reply_text(
            text,
            reply_markup=start_keyboard(resume_exists=False)  # reply-кнопки: створити / інфо
        )
        return end()

async def start_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_state = STATE_ORDER[0]
    context.user_data["state"] = first_state
    first_question = QUESTION_FLOW[first_state][1]

    await update.message.reply_text(f"🔎 {first_question}")
    return first_state

async def new_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_state = STATE_ORDER[0]
    context.user_data["state"] = first_state
    first_question = QUESTION_FLOW[first_state][1]
    message = update.message or update.callback_query.message
    await message.reply_text(f"🔎 {first_question}")
    return first_state

async def send_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = context.user_data.get("resume")
    if not text:
        await query.edit_message_text("❌ Резюме не знайдено. Спробуй згенерувати спочатку.")
        return

    pdf_path = generate_pdf(text)
    with open(pdf_path, "rb") as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="resume.pdf")

    try:
        os.remove(pdf_path)
    except Exception:
        pass




async def edit_markdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 edit_markdown запущено")

    query = update.callback_query
    await query.answer()

    current_text = context.user_data.get("resume")
    logger.warning(f"Збережене резюме (Markdown): {current_text!r}")

    if not current_text:
        logger.warning("❌ Немає тексту для редагування")
        await query.edit_message_text("❌ Немає тексту для редагування.")
        return end()

    logger.info("📤 Надсилаємо запрошення до редагування Markdown")
    await query.message.reply_text("📝 Надішли відредагований Markdown-текст нижче:")

    logger.info("📤 Надсилаємо поточний Markdown у форматі ```")
    await query.message.reply_text(
        f"```markdown\n{current_text}```",
        parse_mode="Markdown"
    )

    logger.info("✅ Перехід у стан EDITING")
    context.user_data["state"] = EDITING  # важливо!
    return EDITING


# Обробка завершеного редагування Markdown
async def edited_markdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"[DEBUG] Прийнято: {update.message}")
    context.user_data['resume'] = update.message.text

    await update.message.reply_text(
        "✅ Текст оновлено. Тепер можна завантажити PDF.",
        reply_markup=result_keyboard()
    )

    return end()


async def regenerate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🔁 Почнімо знову. Як тебе звати?")
    return end() #NAME



async def handle_text(update, context):
    logger.info(f"[handle_text] state={context.user_data.get('state')}")
    user_input = update.message.text
    current_state = context.user_data.get("state", STATE_ORDER[0])
    key = STATE_MAP[current_state]

    context.user_data[key] = user_input

    try:
        next_state = STATE_ORDER[STATE_ORDER.index(current_state) + 1]
    except IndexError:
        await update.message.reply_text("✅ Дані збережено. Генерую резюме...")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        resume = await generate_resume(context.user_data)
        context.user_data['resume'] = resume
        logger.warning(f"FROM Chat {resume}")
        formatted = (
            f"📄 *Твоє згенероване резюме:*\n\n"
            f"*Імʼя:* {context.user_data.get('name')}\n"
            f"*Посада:* {context.user_data.get('position')}\n"
            f"*Освіта:* {context.user_data.get('education')}\n"
            f"*Навички:* {context.user_data.get('skills')}\n"
            f"*Soft-скіли:* {context.user_data.get('soft_skills')}\n"
            f"*Про себе:* {context.user_data.get('about')}"
        )

        await update.message.reply_text(
            # "✅ Резюме готове!\n\nНатисни кнопку нижче 👇",
            formatted,
            parse_mode="Markdown",
            reply_markup=result_keyboard()
        )



        return end()

    context.user_data["state"] = next_state
    next_question = QUESTION_FLOW[next_state][1]
    await update.message.reply_text(next_question)
    return next_state