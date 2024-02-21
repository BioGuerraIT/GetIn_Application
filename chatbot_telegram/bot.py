from telegram.ext import Application
from config import TELEGRAM_BOT_TOKEN, engine
from conversation_handlers import get_conversation_handler
from models import initialize_database

def main():
    initialize_database(engine)  # Create database tables if they don't exist

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(get_conversation_handler())
    application.run_polling()

if __name__ == "__main__":
    main()