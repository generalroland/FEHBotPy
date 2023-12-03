from time import sleep

from pynput.mouse import Button, Controller


class Mouse:
    __instance = None

    @staticmethod
    def get_instance(*args, **kwargs):
        if Mouse.__instance is None:
            Mouse(*args, **kwargs)
        return Mouse.__instance

    def __init__(self, sleep=0):
        if Mouse.__instance is not None:
            raise Exception("This class is a Singleton")
        else:
            Mouse.__instance = self
        self.mouse = Controller()
        self.sleep = sleep

    def get_position(self):
        sleep(self.sleep)
        return self.mouse.position

    def set_position(self, x: int, y: int):
        sleep(self.sleep)
        self.mouse.position = (x, y)

    def left_click(self):
        sleep(self.sleep)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def right_click(self):
        sleep(self.sleep)
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def set_position_and_left_click(self, x: int, y: int):
        self.set_position(x, y)
        self.left_click()

    def set_position_and_right_click(self, x: int, y: int):
        self.set_position(x, y)
        self.right_click()

    def set_position_and_scroll_top(self, x: int, y: int):
        self.set_position(x, y)
        self.mouse.scroll(0, 1)

    def set_position_and_move(self, x: int, y: int, _x: int, _y: int):
        sleep(self.sleep)
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        self.mouse.move(_x, _y)
        sleep(0.6)
        self.mouse.release(Button.left)
