import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, F  # Импортируем F для фильтров
from handlers import cmd_start, cmd_quiz, right_answer, wrong_answer
from utils import create_table

API_TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    await create_table()
    
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")  # Используем F для текстового фильтра
    dp.callback_query.register(right_answer, F.data == "right_answer")  # Используем F для колбэков
    dp.callback_query.register(wrong_answer, F.data == "wrong_answer")  # Используем F для колбэков
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())