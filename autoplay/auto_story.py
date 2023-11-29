import asyncio
import gc
import os
from pathlib import Path

import cv2
import numpy
from mss import mss

from devices import Mouse
from models import *


class AutoStory():
    def __init__(self,
                 bounding_box={
                     "top": 0,
                     "left": 0,
                     "width": 1380,
                     "height": 1400,
                 }, ):
        self.threshold = 0.85
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.bounding_box = bounding_box
        self.patterns = list()
        self.prio_patterns = list()
        self.address_points = list()
        self.mouse = Mouse.get_instance()

    async def screenshot(self):
        self.sct_original = numpy.asarray(self.sct.grab(self.bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    async def load_priority_patterns(self):
        path = str(Path(__file__).parent.parent.absolute()) + "/vision/patterns/priority"
        for file in os.listdir(path):
            img = cv2.imread(f"{path}/{file}", 0)
            self.prio_patterns.append(Pattern(name=file, type='priority', img=img))

    async def load_all_patterns(self, folders: list):
        for folder in folders:
            path = str(Path(__file__).parent.parent.absolute()) + "/vision/patterns/" + folder
            for file in os.listdir(path):
                # print(f"file {path}/{file}")
                img = cv2.imread(f"{path}/{file}", 0)
                self.patterns.append(Pattern(name=file, type=folder, img=img))

    async def clear_patterns(self):
        del self.patterns
        gc.collect()
        self.patterns = list()

    async def match_priority(self):
        await asyncio.sleep(0)
        await self.screenshot()
        for pattern in self.prio_patterns:
            try:
                w, h = pattern.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, pattern.img, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                if max_val >= self.threshold:
                    match_locations = [max_loc]
                    print(f"match_locations {pattern.name} {pattern.type} max_val{max_val} X-{match_locations}")
                    if numpy.asarray(match_locations).size != 0:
                        x = match_locations[-1][0] + w / 2
                        y = match_locations[-1][1] + h / 2
                        self.mouse.set_position_and_left_click(x, y)
                del match
            finally:
                pass

    async def match(self):
        await asyncio.sleep(0)
        await self.screenshot()

        for pattern in self.patterns:
            try:
                w, h = pattern.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, pattern.img, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                if max_val >= self.threshold:
                    match_locations = [max_loc]
                    # print(f"match_locations {pattern.name} {pattern.type} max_val{max_val} X-{match_locations}")
                    if pattern.type in ["priority", "story_mode", "screen", "button"]:
                        if numpy.asarray(match_locations).size != 0:
                            # if pattern.name == "1.bmp":
                            x = match_locations[-1][0] + w / 2
                            y = match_locations[-1][1] + h / 2
                            # self.address_points.append(AddressPoint(x=x, y=y))
                            print(f"match_locations {pattern.name} max_val{max_val} X-{match_locations[-1][0]} Y-{match_locations[-1][1]}")
                            # self.mouse.set_position_and_left_click(x, y)
                    # elif pattern.type == "button":
                    #     if numpy.asarray(match_locations).size != 0:
                    #         x = match_locations[-1][0] + w / 2
                    #         y = match_locations[-1][1] + h / 2
                            self.mouse.set_position_and_left_click(x, y)
                    del match
            finally:
                pass
