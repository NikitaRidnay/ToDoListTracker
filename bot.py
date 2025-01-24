import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import logging
import requests

TOKEN = "7474050367:AAFISYh1aJxS7sUuLlJtTvxPRgMsBW4j49s"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        logger.info(f"Пользователь {user_id} запустил бота")
        await context.bot.send_message(
            chat_id=user_id,
            text="Введите код с сайта для привязки аккаунта:"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        code = update.message.text
        user_id = update.effective_user.id
        logger.info(f"Получен код {code} от пользователя {user_id}")
        
        response = requests.post(
            "http://localhost:5000/link_telegram",
            json={"code": code, "telegram_id": user_id}
        )
        
        if response.status_code == 200 and response.json().get("status") == "success":
            await update.message.reply_text("✅ Аккаунт успешно привязан!")
        else:
            await update.message.reply_text("❌ Неверный код!")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("⚠️ Произошла ошибка")

def setup_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code)
    )
    
    logger.info("Бот запущен!")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application.run_polling()

if __name__ == "__main__":
    setup_bot()