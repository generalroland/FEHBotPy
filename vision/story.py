import asyncio
import gc
import os
import time
from pathlib import Path

import cv2
import numpy
from mss import mss

from devices import Mouse
from models import *


class Story:
    def __init__(self,
                 bounding_box={
                    "top": 42,
                    "left": 2,
                    "width": 540,
                    "height": 960,
                }):
        self.threshold = 0.8
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.bounding_box = bounding_box
        self.patterns = list()
        self.prio_patterns = list()
        self.address_points = list()
        self.mouse = Mouse.get_instance()
        self.patterns_quest = list()
        self.patterns_direction = list()
        self.x = self.bounding_box.get('left') + self.bounding_box.get('width') - 5
        self.y = self.bounding_box.get('top') + 5
        self.quest_bounding_box = {
            "top": 292,
            "left": self.bounding_box.get("left"),
            "width": 120,
            "height": 620,
        }

    async def screenshot(self):
        self.sct = mss()
        self.sct_original = numpy.asarray(self.sct.grab(self.bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    async def get_quest_screenshot(self):
        sct = mss()
        _img = numpy.asarray(sct.grab(self.quest_bounding_box))
        return cv2.cvtColor(_img, cv2.COLOR_BGRA2GRAY)

    async def load_patterns(self, _list: list):
        _folder = str()
        match _list:
            case self.patterns_quest:
                _folder = "quest"
            case self.patterns_direction:
                _folder = "direction"

        _path = str(Path(__file__).parent.absolute()) + f"/patterns/{_folder}"
        for _filename in os.listdir(_path):
            img = cv2.imread(f"{_path}/{_filename}", 0)
            _list.append(Pattern(name=_filename, type=_folder, img=img))

    async def load_priority_patterns(self):
        path = str(Path(__file__).parent.absolute()) + "/patterns/priority"
        for file in os.listdir(path):
            img = cv2.imread(f"{path}/{file}", 0)
            self.prio_patterns.append(Pattern(name=file, type='priority', img=img))

    async def load_all_patterns(self, folders: list):
        for folder in folders:
            path = str(Path(__file__).parent.absolute()) + "/patterns/" + folder
            for file in os.listdir(path):
                # print(f"file {path}/{file}")
                img = cv2.imread(f"{path}/{file}", 0)
                self.patterns.append(Pattern(name=file, type=folder, img=img))

    async def clear_patterns(self):
        del self.patterns
        gc.collect()
        self.patterns = list()

    async def match(self):
        await self.spam_click()
        for prio_pattern in self.prio_patterns:
            try:
                w, h = prio_pattern.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, prio_pattern.img, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                if max_val >= self.threshold:
                    match_locations = [max_loc]
                    if numpy.asarray(match_locations).size != 0:
                        x = match_locations[-1][0] + w / 2 + self.bounding_box.get('left')
                        y = match_locations[-1][1] + h / 2 + self.bounding_box.get('top')
                        self.mouse.set_position_and_left_click(x, y)
                        print(f"{max_val} click {prio_pattern.type} {prio_pattern.name}")
                        del match
                        return
            finally:
                pass
        for _pattern in self.patterns:
            try:
                w, h = _pattern.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, _pattern.img, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                # print(f"{_pattern.type}{_pattern.name} min_val{min_val}, max_val{max_val}, min_loc{min_loc}, max_loc{max_loc}")
                if max_val >= self.threshold:
                    match_locations = [max_loc]
                    if numpy.asarray(match_locations).size != 0:
                        x = match_locations[-1][0] + w / 2 + self.bounding_box.get('left')
                        y = match_locations[-1][1] + h / 2 + self.bounding_box.get('top')
                        self.mouse.set_position_and_left_click(x, y)
                        print(f"{max_val} click {_pattern.type} {_pattern.name}")
                        await asyncio.sleep(0.1)
                        del match
                        return
            finally:
                pass
        # find quest
        await self.find_quest()

    # threshold main quest: 0.80
    async def find_quest(self):
        _timer = time.time()
        while time.time() - _timer < 0.5:
            _sct_img = await self.get_quest_screenshot()
            for _pattern in self.patterns_quest:
                try:
                    w, h = _pattern.img.shape[::-1]
                    match = cv2.matchTemplate(
                        _sct_img, _pattern.img, cv2.TM_CCOEFF_NORMED
                    )
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                    print(f"{_pattern.type}{_pattern.name} min_val{min_val}, max_val{max_val}, min_loc{min_loc}, max_loc{max_loc}")
                    if max_val >= 0.80:
                        match_locations = [max_loc]
                        if numpy.asarray(match_locations).size != 0:
                            x = match_locations[-1][0] + (w - 1) + self.quest_bounding_box.get('left')
                            y = match_locations[-1][1] + (h - 1) + self.quest_bounding_box.get('top')
                            print(f"{max_val} click {max_loc} {_pattern.type} {_pattern.name} ({x},{y})")
                            self.mouse.set_position_and_left_click(x, y)
                            await asyncio.sleep(0.1)
                            del match
                            return
                finally:
                    pass
            # _timer = time.time()
        print(f"not found {time.time() - _timer}")
        x = self.bounding_box.get('left') + 32
        y = self.bounding_box.get('top') + 195
        self.mouse.set_position_and_left_click(x, y)
        print("click back")


    async def spam_click(self):
        self.mouse.set_position_and_left_click(self.x, self.y)