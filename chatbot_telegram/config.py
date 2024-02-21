from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

DATABASE_URL = "sqlite:///user_info.db"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
