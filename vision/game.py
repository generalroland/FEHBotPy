import cv2
import numpy
from mss import mss

from models import Pattern


class Game:
    def __init__(self,
                 bounding_box={
                    "top": 42,
                    "left": 2,
                    "width": 540,
                    "height": 960,
                }):
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.bounding_box = bounding_box

    async def screenshot(self):
        self.sct_original = numpy.asarray(self.sct.grab(self.bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    async def match(self, _pattern: Pattern):
        w, h = _pattern.img.shape[::-1]
        match = cv2.matchTemplate(
            self.sct_img, _pattern.img, cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        return w, h, min_val, max_val, min_loc, max_loc
