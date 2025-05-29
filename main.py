from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from src.bot.handlers import *
from src.core.config import BOT_TOKEN, logger
from src.bot.states import *


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()


    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(filters.Regex("^🚀 Створити резюме$"), start_resume),
            CallbackQueryHandler(edit_markdown, pattern="^edit_markdown$"),
            CallbackQueryHandler(new_resume, pattern="^new_resume$"),
        ],
        states={s: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)] for s in STATE_ORDER} | {
            EDITING: [MessageHandler(filters.TEXT & ~filters.COMMAND, edited_markdown)]
        },
        fallbacks=[CommandHandler("start", start)],

    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(send_pdf, pattern="^generate_pdf$"))
    app.add_handler(CallbackQueryHandler(regenerate, pattern="^regenerate$"))

    logger.info("🚀 Бот запущено. Очікування повідомлень...")
    app.run_polling()


if __name__ == "__main__":
    main()
