import asyncio
import os

from devices import KeyboardListener
from vision import Tutorial


async def autoplay():
    game1 = Tutorial(bounding_box={
        "top": 42,
        "left": 2,
        "width": 540,
        "height": 960,
    })
    game2 = Tutorial(bounding_box={
        "top": 42,
        "left": 546,
        "width": 540,
        "height": 960,
    })
    os.environ['loop'] = '1'
    await game1.load_all_patterns(["rival", "screen", "button"])
    await game2.load_all_patterns(["rival", "screen", "button"])
    while os.environ.get('loop') is not None and os.environ['loop'] == '1':
        await game1.screenshot()
        await game1.match()
        await asyncio.sleep(0)
        await game2.screenshot()
        await game2.match()
        await asyncio.sleep(0)


async def main():
    await autoplay()

if __name__ == "__main__":
    listener = KeyboardListener()

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
