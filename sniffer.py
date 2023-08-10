from handler.channel_handler import TwitchChannelHandler
from handler.browser_handler import BrowserHandler
from handler.timer_handler import Timer


class Sniffer:
    def __init__(self, channels: list, browser_path: str):
        self._channels = channels
        self._browser_path = browser_path
        self._channel_search_timer = Timer(interval_seconds=30)
        self._channel_reset_timer = Timer(interval_seconds=600)
        self._browser_handler = BrowserHandler(browser_path=self._browser_path)
        self._channel_handler = TwitchChannelHandler(channel_list=self._channels)
        self._active_channel = None
        self._browser_open = False
        self._new_channel = False

    @property
    def browser_open(self) -> bool:
        return self._browser_open

    @property
    def active_channel(self) -> str:
        return self._active_channel

    @property
    def new_channel(self) -> bool:
        if self._new_channel:
            self._new_channel = False
            return True
        return False

    def check(self) -> bool:
        # returns True if any action was taken
        if not self._browser_open:
            self._channel_search_timer.set_temp_and_reset(0)

        # reset routine
        if self._channel_reset_timer.check_and_reset():
            self._browser_handler.browser_close()
            self._active_channel = None
            self._browser_open = False
            return True

        # checking routine
        if self._channel_search_timer.check_and_reset():
            online_channel = self._channel_handler.channel_search()
            if online_channel is not None and online_channel != self._active_channel:
                self._new_channel = True
                self._active_channel = online_channel
                self._browser_handler.browser_open(url=f"https://www.twitch.tv/{online_channel}")
                self._browser_open = True
            if online_channel is None:
                self._browser_handler.browser_close()
                self._browser_open = False
            return True

        return False

    def stop(self):
        try:
            self._browser_handler.browser_close()
        except Exception:
            pass



