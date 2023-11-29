import os
import signal
import threading

from pynput.keyboard import Key, Listener


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press)
        threading.Thread(target=self.listen).start()

    def listen(self):
        with self.listener as listener:
            listener.join()

    def on_press(self, key):

        # if key == Key.backspace:
        #     Shop.buy_build(self.build.item_build)

        if key == Key.home:
            os.environ['loop'] = "1" if os.environ['loop'] == "0" else "1"

        if key == Key.end:
            pid = int(os.getpid())
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                os.system(f"taskkill /f /pid {pid}")
            return False
