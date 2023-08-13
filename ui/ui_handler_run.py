import time

from sniffer import Sniffer
from ui.ui_handler_main import UIHandlerMain, UICleaner


class UIHandlerRun:
    def __init__(self, channels: list, browser_path: str):
        self._channels = channels
        self._browser_path = browser_path
        self._channels = channels
        self._spacer = " " * 10
        self._running = True

    @staticmethod
    def get_current_time_string() -> str:
        time_struct = time.localtime()
        time_string = f"{time_struct.tm_hour:02d}:{time_struct.tm_min:02d}:{time_struct.tm_sec:02d}: "
        return time_string

    def _sniffer_action(self, sniffer: Sniffer) -> None:
        if sniffer.active_channel is None:
            print(f"{self.get_current_time_string()}Sniffer did not sniff any channel")
            print(f"{self._spacer}Idling ...\n")
            return
        if sniffer.new_channel:
            print(f"{self.get_current_time_string()}Sniffer sniffed {sniffer.active_channel}'s channel")
            print(f"{self._spacer}Opening browser ...\n")
            return
        print(f"{self.get_current_time_string()}Sniffer found {sniffer.active_channel}'s channel is still online\n")
        return

    def _sniffer_routine(self) -> None:
        UICleaner.clear_console()
        UIHandlerMain.show_logo()
        print(" - Channels")
        UIHandlerMain.print_channel_bar(self._channels, end="\n")
        print(f"{self.get_current_time_string()}Sniffer starting")
        print(f"{self._spacer}Press 'Ctrl + C' to stop anytime\n")
        sniffer = Sniffer(self._channels, self._browser_path)
        try:
            while self._running:
                if sniffer.check():
                    self._sniffer_action(sniffer)
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            sniffer.stop()
            print(f"{self.get_current_time_string()}Sniffer stopping\n")

    def run(self) -> None:
        self._sniffer_routine()
        print(f"{self.get_current_time_string()}Sniffer stopped successfully\n")
        input("Press a key to exit")
