import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

REDIS_PORT = os.environ.get("REDIS_PORT")

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

CHAT_ID = os.environ.get("CHAT_ID")
USER_ID = os.environ.get("USER_ID")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")

IDENT_YANDEX_CLOUD = os.environ.get("IDENT_YANDEX_CLOUD")
KEY_YANDEX_CLOUD = os.environ.get("KEY_YANDEX_CLOUD")
BUCKET = os.environ.get("BUCKET")


