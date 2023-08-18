import abc
import pathlib
from typing import Union

from utils.debug_utils import Debugger
from youtube_crawler.page_parser import YoutubePageParser
from youtube_crawler.browser_agent import YoutubeBrowserAgent


class YoutubeBaseCrawler:
    def __init__(self, headless=False, debug_tool: Debugger = None, interactor_config_path: Union[str, pathlib.Path] = None):
        self._browser_agent = YoutubeBrowserAgent(headless=headless, debug_tool=debug_tool, interactor_config_path=interactor_config_path)
        self._page_parser = YoutubePageParser(browser_agent=self._browser_agent)

    async def start(self) -> None:
        await self._browser_agent.start()

    async def stop(self) -> None:
        await self._browser_agent.stop()

    @abc.abstractmethod
    def crawl(self, *args, **kwargs):
        raise NotImplementedError


__all__ = ["YoutubeBaseCrawler"]
