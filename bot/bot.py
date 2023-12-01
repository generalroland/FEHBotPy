import asyncio
import os

from vision.story import Story


class Bot:

    async def autoplay(self):
        game1 = Story(bounding_box={
            "top": 42,
            "left": 2,
            "width": 540,
            "height": 960,
        })
        game2 = Story(bounding_box={
            "top": 42,
            "left": 546,
            "width": 540,
            "height": 960,
        })
        os.environ['loop'] = '1'
        await game1.load_priority_patterns()
        await game1.load_all_patterns(["story_mode", "screen", "button", "quest"])
        await game2.load_priority_patterns()
        await game2.load_all_patterns(["story_mode", "screen", "button", "quest"])
        while os.environ.get('loop') is not None and os.environ['loop'] == '1':
            await game1.match()
            await asyncio.sleep(0)
            await game2.match()
            await asyncio.sleep(0)
