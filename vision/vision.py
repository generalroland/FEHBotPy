import gc
import os
from pathlib import Path

import cv2
import numpy
from mss import mss

from models import *


class Vision:
    def __init__(self,
                 bounding_box={
                     "top": 0,
                     "left": 0,
                     "width": 3440,
                     "height": 1440,
                 }, ):
        self.threshold = 0.7
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.bounding_box = bounding_box
        self.patterns = list()
        self.matches = list()
        self.address_points = list()
        self.path = str(Path(__file__).parent.parent.absolute())

    async def screenshot(self):
        self.sct_original = numpy.asarray(self.sct.grab(self.bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    async def load_all_patterns(self, folder: str):
        path = self.path + "/vision/patterns/" + folder
        print("path")
        for file in os.listdir(path):
            # print(f"file {path}/{file}")
            img = cv2.imread(f"{path}/{file}", 0)
            self.patterns.append(Pattern(name=file, type=folder, img=img))

    async def load_template(self, folder: str, names: list):
        path = str(Path(__file__).parent.absolute()) + "/patterns"
        for name in names:
            # print(f"{path}/{folder}/{name}.bmp")
            img = cv2.imread(f"{path}/{folder}/{name}.bmp", 0)
            self.patterns.append(Pattern(name=name, img=img))

    async def clear_patterns(self):
        del self.patterns
        gc.collect()
        self.patterns = list()

    async def clear_matches(self):
        del self.matches
        gc.collect()
        self.matches = list()

    async def match(self):
        for pattern in self.patterns:
            try:
                w, h = pattern.img.shape[::-1]
                print(f"w-{w} h-{h}")
                match = cv2.matchTemplate(
                    self.sct_img, pattern.img, cv2.TM_CCOEFF_NORMED
                )
                if pattern.name == "close":
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                    print(f"min_val {min_val} max_val {max_val} min_loc{min_loc} max_loc{max_loc}")

                    match_locations = numpy.where(match > self.threshold)
                    # print(f"match_locations {match_locations}")

                    for (x, y) in zip(match_locations[1], match_locations[0]):
                        self.address_points.append(AddressPoint(x=x + w / 2, y=y + h / 2))

                    # for point in max_loc:
                    #     x = int( point[0] + int(w / 2))
                    #     y = int( point[1] + int(h / 2))
                    #     print(f"x-{x} y-{y}")
                    # if max_val > 0.99 and max_loc[0] > 0:
                    #     print(f"max_loc {max_loc}")
                    #     self.address_points.append(AddressPoint(x=max_loc[0] + int(w / 2)), y=max_loc[1] + int(h / 2))
                    # continue
            finally:
                pass
