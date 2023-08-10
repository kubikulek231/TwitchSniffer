import requests
from bs4 import BeautifulSoup
import time


class TwitchChannelHandler:
    URL = "https://decapi.me/twitch/uptime/"

    def __init__(self, channel_list: list):
        self._channel_list = channel_list

    @staticmethod
    def _get_html_str(url, max_retries: int = 5, retry_delay: int = 2) -> str:
        retries = 0
        while retries < max_retries:
            response = requests.get(url)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')
                return str(soup)
            else:
                retries += 1
                time.sleep(retry_delay)

    def channel_search(self) -> str:
        for channel in self._channel_list:
            url = self.URL + channel
            html_str = self._get_html_str(url)
            if "offline" not in html_str:
                return channel

