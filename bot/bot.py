import asyncio
import os

from vision.story import Story


class Bot:

    async def autoplay(self):
        game1 = Story(bounding_box={
            "top": 288,
            "left": 2,
            "width": 624,
            "height": 1110,
        })
        game2 = Story(bounding_box={
            "top": 288,
            "left": 630,
            "width": 624,
            "height": 1110,
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
