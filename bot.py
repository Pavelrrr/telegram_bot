import aiosqlite
import logging
from aiogram import Bot, Dispatcher

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7192262474:AAE1_SqT5bPJ5iWCKMONce4QZN57DxNHhFY'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

DB_NAME = 'quiz_bot.db'