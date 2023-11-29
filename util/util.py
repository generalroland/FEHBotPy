import time
from typing import Generator

from psutil import Process, process_iter, NoSuchProcess, ZombieProcess


class Util:
    def return_ux_process(self) -> Generator[Process, None, None]:
        for process in process_iter():
            try:
                if process.name() == "Bluestacks.exe":
                    yield process
            except NoSuchProcess:
                continue
            except ZombieProcess:
                continue

    def get_process(self):
        process = next(self.return_ux_process(), None)
        while not process:
            process = next(self.return_ux_process(), None)
            print("Process not found, start the client")
            time.sleep(1)
