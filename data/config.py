from dotenv import load_dotenv
import os
import json

# environs kutubxonasidan foydalanish
load_dotenv()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Bot token
ADMINS = json.loads(os.environ.get("ADMINS"))  # adminlar ro'yxati
IP = os.environ.get("ip")  # Xosting ip manzili

DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
