import asyncio
import os

from autoplay import AutoStory


class Bot:
    def __init__(self):
        self.auto_story = AutoStory()
        loop = asyncio.get_event_loop()
        loop.create_task(self.bot_loop())

    async def bot_loop(self):
        os.environ['loop'] = '1'
        await self.auto_story.load_priority_patterns()
        await self.auto_story.load_all_patterns(["story_mode", "screen", "button"])
        while os.environ.get('loop') is not None and os.environ['loop'] == '1':
            await self.autoplay()
            await asyncio.sleep(0)

    async def autoplay(self):
        await self.auto_story.match_priority()
        await asyncio.sleep(0)
        await self.auto_story.match()
