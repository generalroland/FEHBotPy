import asyncio

from bot import Bot
from devices import KeyboardListener


async def main():
    bot = Bot()
    await bot.autoplay()
    # await bot.test()

if __name__ == "__main__":
    listener = KeyboardListener()

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
