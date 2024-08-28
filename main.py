import asyncio
from bot import create_table, bot, dp
from handlers import router


async def main():
    dp.include_router(router)
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())