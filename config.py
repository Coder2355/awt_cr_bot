
import os

class Config:
    API_ID = os.getenv("API_ID", "21740783")  # Your Telegram API ID
    API_HASH = os.getenv("API_HASH", "a5dc7fec8302615f5b441ec5e238cd46")  # Your Telegram API hash
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7444872585:AAHYzPX_gygFh9xYvu0-k7YOUg7BSG_hzHg")  # Your bot token from BotFather
    GOGOANIME_API_URL = "https://gogoanime.api"  # Base URL for Gogoanime API

config = Config()
