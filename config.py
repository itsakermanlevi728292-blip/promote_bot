import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///promote.db")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
DEFAULT_LOG_CHANNEL = os.getenv("LOG_CHANNEL_ID")
