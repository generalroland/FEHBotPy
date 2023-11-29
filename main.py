import asyncio

from bot import Bot
from devices import KeyboardListener


async def main():
    bot = Bot()
    await bot.bot_loop()
    # util = Util()
    # vision = Vision()
    # mouse = Mouse.get_instance()
    # # await vision.clear_matches()
    # # await vision.clear_patterns()
    # # await vision.load_template(folder="button", names=["close"])
    # # await vision.screenshot()
    # # await vision.match()
    # #
    # # for address_point in vision.address_points:
    # #     print(f"close: x-{address_point.x} y-{address_point.y}")
    # #     # mouse.set_position_and_left_click(address_point.x, address_point.y)
    # # await asyncio.sleep(1)
    # autobot = AutoStory()
    # await autobot.load_all_patterns("button")
    # await autobot.screenshot()
    # await autobot.match()
    # for address_point in autobot.address_points:
    #     mouse.set_position_and_left_click(address_point.x, address_point.y)

    # await vision.load_all_patterns("button")

if __name__ == "__main__":
    listener = KeyboardListener()

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
