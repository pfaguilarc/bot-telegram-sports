import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
    API_FOOTBALL_HOST = os.getenv("API_FOOTBALL_HOST", "v3.football.api-sports.io")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bot.db")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()