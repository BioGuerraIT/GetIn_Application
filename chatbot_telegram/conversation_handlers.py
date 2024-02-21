from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from constants import *
from handlers import start, update, cancel, first_name, last_name, email, age, school, preferences, bio, update_choice, update_first_name, update_last_name, update_email, update_age, update_school, update_preferences, update_bio

def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("update", update)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            SCHOOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, school)],
            PREFERENCES: [MessageHandler(filters.TEXT & ~filters.COMMAND, preferences)],
            UPDATE_CHOICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_choice)
            ],
            UPDATE_FIRST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_first_name)
            ],
            UPDATE_LAST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_last_name)
            ],
            UPDATE_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_email)
            ],
            UPDATE_BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_bio)],
            UPDATE_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_age)],
            UPDATE_SCHOOL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_school)
            ],
            UPDATE_PREFERENCES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_preferences)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )