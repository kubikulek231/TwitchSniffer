import os
import subprocess

import psutil


class BrowserHandler:

    def __init__(self, browser_path: str):
        self._browser_path = browser_path

    @staticmethod
    def browser_is_path_correct(path: str) -> bool:
        return os.path.isfile(path)

    def browser_open(self, url: str) -> None:
        try:
            browser_cmd = self._browser_path
            browser_args = [browser_cmd, "--new-window", url]
            psutil.Popen(browser_args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except Exception as e:
            print(f"Error opening browser: {e}")
            return None

    def browser_close(self) -> None:
        for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                if os.path.basename(self._browser_path) in process.name():
                    psutil.Process(process.pid).terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print("Error closing browser:\n" + e)
                pass
